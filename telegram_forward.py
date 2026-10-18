"""
Telegram Message Forwarder

A script for mass forwarding messages from one Telegram group/channel to another.
Works as a userbot (from your account), no need to add bots to groups.

Features:
- Saves progress to file — can stop (Ctrl+C) and resume later
- Automatically handles FloodWait errors
- Logs to console and file
- Safe delays between messages to avoid bans
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("❌ python-dotenv not installed!")
    print("   Run: pip install python-dotenv")
    sys.exit(1)

try:
    from telethon import TelegramClient
    from telethon.errors import FloodWaitError, ChatForwardsRestrictedError
except ImportError:
    print("❌ Telethon not installed!")
    print("   Run: pip install telethon")
    sys.exit(1)

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# CONFIGURATION (loaded from .env file)
# ============================================================================

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
SOURCE_CHAT = os.getenv('SOURCE_CHAT')
DEST_CHAT = os.getenv('DEST_CHAT')
DELAY_BETWEEN_MESSAGES = float(os.getenv('DELAY_BETWEEN_MESSAGES', '1.5'))
PROGRESS_FILE = os.getenv('PROGRESS_FILE', 'forward_progress.json')

# Validate configuration
def validate_config():
    """Check that all required configuration is present."""
    errors = []
    
    if not API_ID:
        errors.append("API_ID is not set")
    elif not API_ID.isdigit():
        errors.append("API_ID must be a number")
    
    if not API_HASH:
        errors.append("API_HASH is not set")
    
    if not SOURCE_CHAT:
        errors.append("SOURCE_CHAT is not set")
    
    if not DEST_CHAT:
        errors.append("DEST_CHAT is not set")
    
    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"   • {error}")
        print("\n📝 Please check your .env file")
        print("   See .env.example for reference")
        sys.exit(1)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('forward_log.txt', encoding='utf-8')
    ]
)
log = logging.getLogger(__name__)


def parse_chat_id(chat_id: str):
    """Parse chat ID from string (can be numeric ID or @username)."""
    chat_id = chat_id.strip()
    if chat_id.lstrip('-').isdigit():
        return int(chat_id)
    return chat_id  # Return as username


def load_progress() -> dict:
    """Load progress from file."""
    if Path(PROGRESS_FILE).exists():
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {'last_id': 0, 'forwarded_count': 0, 'started_at': None}


def save_progress(last_id: int, count: int, started_at: str):
    """Save progress to file."""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({
            'last_id': last_id,
            'forwarded_count': count,
            'started_at': started_at
        }, f, indent=2)


async def get_total_messages(client, chat) -> int:
    """Get approximate total message count in chat."""
    async for msg in client.iter_messages(chat, limit=1):
        return msg.id
    return 0


async def forward_with_retry(client, dest, message, max_retries=3):
    """Forward a message with retry on errors."""
    for attempt in range(max_retries):
        try:
            await client.forward_messages(dest, message)
            return True
        except FloodWaitError as e:
            wait_time = e.seconds + 10  # +10 seconds for safety
            log.warning(f"⏳ FloodWait! Waiting {wait_time} sec ({wait_time // 60} min)...")
            await asyncio.sleep(wait_time)
        except ChatForwardsRestrictedError:
            log.error("❌ Forwarding is restricted in the source chat!")
            return False
        except Exception as e:
            log.error(f"⚠️ Error: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(5)
            else:
                return False
    return False


# ============================================================================
# MAIN FUNCTION
# ============================================================================

async def main():
    validate_config()
    
    source_chat = parse_chat_id(SOURCE_CHAT)
    dest_chat = parse_chat_id(DEST_CHAT)
    
    log.info("=" * 50)
    log.info("🚀 Telegram Message Forwarder")
    log.info("=" * 50)
    
    # Load progress
    progress = load_progress()
    last_forwarded_id = progress['last_id']
    forwarded_count = progress['forwarded_count']
    started_at = progress['started_at'] or datetime.now().isoformat()
    
    if last_forwarded_id > 0:
        log.info(f"📂 Found saved progress: {forwarded_count} messages")
        log.info(f"   Resuming from ID > {last_forwarded_id}")
    
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    client = TelegramClient('session', int(API_ID), API_HASH)
    await client.start(bot_token=BOT_TOKEN)

        # Check authorization
        me = await client.get_me()
        log.info(f"✅ Logged in as: {me.first_name} (@{me.username})")
        
        # Get chat info
        try:
            source = await client.get_entity(source_chat)
            dest = await client.get_entity(dest_chat)
            source_title = getattr(source, 'title', getattr(source, 'first_name', 'Unknown'))
            dest_title = getattr(dest, 'title', getattr(dest, 'first_name', 'Unknown'))
            log.info(f"📤 Source: {source_title}")
            log.info(f"📥 Destination: {dest_title}")
        except Exception as e:
            log.error(f"❌ Failed to get chat info: {e}")
            log.error("   Check chat IDs and make sure you're a member of both chats")
            return
        
        # Count total messages
        total = await get_total_messages(client, source_chat)
        log.info(f"📊 Total messages in source: ~{total}")
        
        # Collect messages (oldest first)
        log.info("📋 Loading message list...")
        messages = []
        async for msg in client.iter_messages(source_chat, reverse=True, min_id=last_forwarded_id):
            messages.append(msg)
        
        remaining = len(messages)
        log.info(f"📋 Messages to forward: {remaining}")
        
        if remaining == 0:
            log.info("✅ All messages already forwarded!")
            return
        
        # Time estimate
        estimated_seconds = remaining * (DELAY_BETWEEN_MESSAGES + 0.5)
        estimated_hours = estimated_seconds / 3600
        log.info(f"⏱️ Estimated time: {estimated_hours:.1f} hours")
        log.info("-" * 50)
        
        # Main forwarding loop
        for i, msg in enumerate(messages, 1):
            # Skip service messages (join/leave, etc.)
            if msg.action is not None:
                continue
            
            success = await forward_with_retry(client, dest_chat, msg)
            
            if success:
                forwarded_count += 1
                last_forwarded_id = msg.id
                
                # Save progress every 10 messages
                if forwarded_count % 10 == 0:
                    save_progress(last_forwarded_id, forwarded_count, started_at)
                
                # Log every 50 messages or at start
                if forwarded_count % 50 == 0 or forwarded_count <= 5:
                    progress_pct = (i / remaining) * 100
                    log.info(f"📨 Forwarded: {forwarded_count} | Progress: {progress_pct:.1f}%")
            else:
                log.warning(f"⚠️ Skipped message ID {msg.id}")
            
            # Delay between messages
            await asyncio.sleep(DELAY_BETWEEN_MESSAGES)
        
        # Final save
        save_progress(last_forwarded_id, forwarded_count, started_at)
        
        log.info("=" * 50)
        log.info(f"✅ Done! Forwarded messages: {forwarded_count}")
        log.info("=" * 50)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("\n⏸️ Stopped by user. Progress saved.")
        log.info("   Run the script again to resume.")

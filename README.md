# Telegram Message Forwarder

A Python script for mass forwarding messages from one Telegram chat to another. Works as a userbot (using your account), so no need to add any bots to groups.

### Working on 01.02.2026

[🇷🇺 Русская версия](#русская-версия)

## Features

-   ✅ Forward messages with all media (photos, videos, voice messages, files, etc.)
-   ✅ **Progress saving** — stop anytime (Ctrl+C) and resume later
-   ✅ **Automatic FloodWait handling** — waits when Telegram asks to slow down
-   ✅ Works with private groups (no bot needed)
-   ✅ Preserves chronological order
-   ✅ Detailed logging to console and file

### Supported chat types

- ✅ Private chats (1-on-1)
- ✅ Groups / Supergroups
- ✅ Channels (admin rights required to forward **to** a channel)

## Requirements

-   Python 3.8+
-   Telegram account
-   API credentials from [my.telegram.org](https://my.telegram.org)

## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/telegram-forward-bot.git
    cd telegram-forward-bot
    ```

2. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Get Telegram API credentials**

    - Go to [my.telegram.org](https://my.telegram.org)
    - Log in with your phone number
    - Go to "API development tools"
    - Create an application (any name/platform)
    - Copy `App api_id` and `App api_hash`

4. **Get chat IDs**

    - Forward any message from your source/destination chat to [@userinfobot](https://t.me/userinfobot)
    - The bot will reply with the chat ID
    - Supergroup IDs look like `-1001234567890`

5. **Configure the script**

    ```bash
    cp .env.example .env
    ```

    Edit `.env` file and fill in your values:

    ```env
    API_ID=12345678
    API_HASH=your_api_hash_here
    SOURCE_CHAT=-1001234567890
    DEST_CHAT=-1009876543210
    ```

## Usage

```bash
python telegram_forward.py
```

On first run, you'll be asked to:

1. Enter your phone number
2. Enter the code sent to your Telegram
3. Enter 2FA password (if enabled)

After that, the session is saved and you won't need to log in again.

### Stopping and Resuming

-   Press `Ctrl+C` to stop the script
-   Progress is automatically saved every 10 messages
-   Just run the script again to resume from where you left off

## Configuration Options

| Variable                 | Description                       | Default                 |
| ------------------------ | --------------------------------- | ----------------------- |
| `API_ID`                 | Telegram API ID                   | required                |
| `API_HASH`               | Telegram API Hash                 | required                |
| `SOURCE_CHAT`            | Source chat ID or @username       | required                |
| `DEST_CHAT`              | Destination chat ID or @username  | required                |
| `DELAY_BETWEEN_MESSAGES` | Delay in seconds between messages | `1.5`                   |
| `PROGRESS_FILE`          | File to save progress             | `forward_progress.json` |

## Time Estimates

With default 1.5s delay:

-   1,000 messages ≈ 30 minutes
-   10,000 messages ≈ 5 hours
-   50,000 messages ≈ 24 hours

Plus potential FloodWait pauses (usually 10-50 minutes after every ~2000-3000 messages).

## From the developer (me)

-   I advise you to use a delay of 2 - 2.5 seconds instead of 1.5, in order to avoid unnecessary timeouts and, in rare cases, to block your account for 24 hours (or more if you continue to use a delay of less than 1.5 seconds).
-   If you are forwarding more than 1000 messages, there may be timeouts for several seconds during loading, such as: "Sleeping for 3s (0:00:03) on GetHistoryRequest flood wait" - this will be written in the terminal. This is fine, just wait for the bot to download all the messages, and something like "Messages to forward: 10625, Estimated time: 7.4 hours" will appear, which means that progress has started. Pour the tea!

## Security Notes

⚠️ **Never share these files:**

-   `.env` — contains your API credentials
-   `*.session` — contains your authorized session

Anyone with these files can access your Telegram account!

## Limitations

-   Cannot forward from chats with "Restrict saving content" enabled
-   Forwarded messages show "Forwarded from" header
-   Some metadata is lost: reactions, poll votes, reply context
-   You must be in the chat rooms from which and where the messages are being forwarded

## License

MIT License — feel free to use, modify, and distribute.

---

# Русская версия

Python-скрипт для массовой пересылки сообщений из одного чата Telegram в другой. Работает как юзербот (от вашего аккаунта), не требует добавления ботов в группы.

### Работает 01.02.2026

## Возможности

-   ✅ Пересылка сообщений со всеми медиа (фото, видео, голосовые, файлы и т.д.)
-   ✅ **Сохранение прогресса** — можно остановить (Ctrl+C) и продолжить позже
-   ✅ **Автоматическая обработка FloodWait** — ждёт, когда Telegram просит притормозить
-   ✅ Работает с приватными группами (бот не нужен)
-   ✅ Сохраняет хронологический порядок
-   ✅ Подробное логирование в консоль и файл

###Поддерживаемые типы чатов

-    ✅ Личные чаты (1-на-1)
-    ✅ Группы / Супергруппы
-    ✅ Каналы (нужны права админа для пересылки в канал)

## Требования

-   Python 3.8+
-   Аккаунт Telegram
-   API credentials с [my.telegram.org](https://my.telegram.org)

## Установка

1. **Клонируйте репозиторий**

    ```bash
    git clone https://github.com/yourusername/telegram-forward-bot.git
    cd telegram-forward-bot
    ```

2. **Установите зависимости**

    ```bash
    pip install -r requirements.txt
    ```

3. **Получите API credentials**

    - Перейдите на [my.telegram.org](https://my.telegram.org)
    - Войдите по номеру телефона
    - Перейдите в "API development tools"
    - Создайте приложение (название/платформа — любые)
    - Скопируйте `App api_id` и `App api_hash`

4. **Узнайте ID чатов**

    - Перешлите любое сообщение из нужного чата боту [@userinfobot](https://t.me/userinfobot)
    - Бот ответит с ID чата
    - ID супергрупп выглядят примерно как `-1001234567890`

5. **Настройте скрипт**

    ```bash
    cp .env.example .env
    ```

    Отредактируйте файл `.env`:

    ```env
    API_ID=12345678
    API_HASH=your_api_hash_here
    SOURCE_CHAT=-1001234567890
    DEST_CHAT=-1009876543210
    ```

## Использование

```bash
python telegram_forward.py
```

При первом запуске нужно:

1. Ввести номер телефона
2. Ввести код из Telegram
3. Ввести пароль 2FA (если включён)

После этого сессия сохраняется, повторный вход не потребуется.

### Остановка и продолжение

-   Нажмите `Ctrl+C` для остановки
-   Прогресс автоматически сохраняется каждые 10 сообщений
-   Просто запустите скрипт снова, чтобы продолжить с того же места

## Параметры конфигурации

| Переменная               | Описание                         | По умолчанию            |
| ------------------------ | -------------------------------- | ----------------------- |
| `API_ID`                 | Telegram API ID                  | обязательно             |
| `API_HASH`               | Telegram API Hash                | обязательно             |
| `SOURCE_CHAT`            | ID или @username исходного чата  | обязательно             |
| `DEST_CHAT`              | ID или @username целевого чата   | обязательно             |
| `DELAY_BETWEEN_MESSAGES` | Задержка между сообщениями (сек) | `1.5`                   |
| `PROGRESS_FILE`          | Файл для сохранения прогресса    | `forward_progress.json` |

## Оценка времени

При задержке 1.5 сек:

-   1 000 сообщений ≈ 30 минут
-   10 000 сообщений ≈ 5 часов
-   50 000 сообщений ≈ 24 часа

Плюс возможные паузы на FloodWait (обычно 10-50 минут после каждых ~2000-3000 сообщений).

## От разработчика (меня)

-   Советую использовать задержку 2 - 2.5 секунды, вместо 1.5, во избежание лишних таймаутов и в редких случаях блокировке аккаунта на 24 часа (и более, если продолжите использовать задержку меньше 1.5с.)
-   Если вы пересылаете больше 1000 сообщений, то при загрузке могут быть таймауты на несколько секунд, по типу: "Sleeping for 3s (0:00:03) on GetHistoryRequest flood wait" - это напишет в терминале. Это нормально, просто дождитесь пока бот загрузит все сообщения, и высветится что-то вроде: "Messages to forward: 10625, Estimated time: 7.4 hours" - это значит, что прогресс пошёл. Наливайте чай!

## Безопасность

⚠️ **Никогда не делитесь этими файлами:**

-   `.env` — содержит ваши API credentials
-   `*.session` — содержит авторизованную сессию

С этими файлами можно получить доступ к вашему аккаунту!

## Ограничения

-   Не работает с чатами с включённой опцией "Запретить сохранение контента"
-   Пересланные сообщения показывают заголовок "Переслано от"
-   Некоторые данные теряются: реакции, голоса в опросах, контекст ответов
-   Вы должны быть в чатах из которого, и куда пересылаются сообщения

## Лицензия

MIT License — свободно используйте, модифицируйте и распространяйте.

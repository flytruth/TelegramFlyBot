# TelegramFlyBot

A small Telegram bot template built with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).
Good starting point if you want a working bot with commands, buttons, and message handling without writing everything from scratch.

## Features

- Basic commands: `/start`, `/help`, `/jump`, `/about`, `/time`, `/echo`
- Inline buttons for quick actions
- Simple keyword-based auto replies
- Per-user message stats (in memory)
- Works in private chats and groups (with mention)
- Logging + error handler

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/yourname/TelegramFlyBot.git
   cd TelegramFlyBot
   ```

2. Install dependencies:
   ```bash
   pip install python-telegram-bot
   ```

3. Put your bot token in the code (or better, use an environment variable):
   ```python
   TOKEN = "YOUR_BOT_TOKEN"
   ```

4. Run:
   ```bash
   python bot.py
   ```

## Commands

| Command | What it does |
|---|---|
| `/start` | Greets you and shows buttons |
| `/help` | Lists all commands |
| `/jump` | Makes the bot jump |
| `/channels` | Shows recommended channels |
| `/stats` | Your message count |
| `/about` | Info about the bot |
| `/echo <text>` | Repeats your text |
| `/time` | Current server time |

## How it works

- `handle_response()` checks for keywords like `hello`, `how are you`, `thanks`, etc. and returns a reply.
- In groups, the bot only replies when it's mentioned (`@kfspE55_bot`).
- `user_stats` is a plain dict — it resets every time the bot restarts. Swap it for SQLite if you want persistence.

## Notes

- The token in the code is a placeholder — replace it with your own.
- Never commit real tokens to GitHub. Use a `.env` file or environment variables.

## License

MIT — do whatever you want with it.

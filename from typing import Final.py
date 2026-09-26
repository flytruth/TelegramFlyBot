import logging
from typing import Final
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

# --- Config ---
TOKEN: Final = ''
BOT_USERNAME: Final = ''

CHANNELS = ["@muslim_guy", "@bexind_studio", "@DanielPsenicni"]

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Simple stats storage (resets when bot restarts)
user_stats = {}


def track(update: Update):
    user = update.effective_user
    if not user:
        return
    if user.id not in user_stats:
        user_stats[user.id] = {
            "name": user.username or user.full_name,
            "messages": 0,
            "since": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    user_stats[user.id]["messages"] += 1


def main_keyboard():
    buttons = [
        [InlineKeyboardButton("Channels", callback_data="channels"),
         InlineKeyboardButton("About", callback_data="about")],
        [InlineKeyboardButton("Help", callback_data="help"),
         InlineKeyboardButton("Stats", callback_data="stats")],
    ]
    return InlineKeyboardMarkup(buttons)


# --- Commands ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track(update)
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"Hi {name}! This bot is for your statistics (:\n"
        f"Type /help or use the buttons below.",
        reply_markup=main_keyboard(),
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track(update)
    await update.message.reply_text(
        "Commands:\n"
        "/start - start the bot\n"
        "/help - this message\n"
        "/jump - make the bot jump\n"
        "/channels - list my channels\n"
        "/stats - your message count\n"
        "/about - about the bot\n"
        "/echo <text> - repeat text\n"
        "/time - current server time"
    )


async def jump(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track(update)
    await update.message.reply_text("You have jumped! Boing boing 🦘")


async def channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track(update)
    text = "My channels:\n" + "\n".join(f"{i+1}) {c}" for i, c in enumerate(CHANNELS))
    await update.message.reply_text(text)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track(update)
    data = user_stats.get(update.effective_user.id, {})
    await update.message.reply_text(
        f"Username: @{data.get('name', '?')}\n"
        f"Messages: {data.get('messages', 0)}\n"
        f"First seen: {data.get('since', '?')}"
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track(update)
    await update.message.reply_text(
        f"TelegramFlyBot\n"
        f"A small bot template made with python-telegram-bot.\n"
        f"Bot: {BOT_USERNAME}"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track(update)
    if not context.args:
        await update.message.reply_text("Usage: /echo <text>")
        return
    await update.message.reply_text(" ".join(context.args))


async def time_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track(update)
    await update.message.reply_text(datetime.now().strftime("Server time: %Y-%m-%d %H:%M:%S"))


# --- Response logic ---

def get_response(text: str) -> str:
    t = text.lower()
    if "hello" in t or "hi" in t:
        return "Hey there!"
    if "how are you" in t:
        return "I am fine, and you?"
    if "good" in t:
        return "Nice! Can you subscribe to @bexind_studio ?"
    if "no" in t:
        return "You are обезьяна 🐒"
    if "thanks" in t or "thank you" in t:
        return "You're welcome!"
    if "bye" in t:
        return "Bye! Come back soon."
    return "I don't understand. Type /help or /start"


# --- Message / button handlers ---

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return

    track(update)
    chat_type = msg.chat.type
    text = msg.text

    logger.info(f"{msg.chat.id} [{chat_type}]: {text}")

    # Reply in private chats, or when mentioned in groups
    if chat_type == "private" or BOT_USERNAME.lower() in text.lower():
        reply = get_response(text)
        logger.info(f"Reply: {reply}")
        await msg.reply_text(reply)


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "channels":
        text = "My channels:\n" + "\n".join(f"{i+1}) {c}" for i, c in enumerate(CHANNELS))
        await query.edit_message_text(text)

    elif data == "about":
        await query.edit_message_text(f"TelegramFlyBot\nBot: {BOT_USERNAME}")

    elif data == "help":
        await query.edit_message_text("Use /help to see all commands.")

    elif data == "stats":
        info = user_stats.get(query.from_user.id, {})
        await query.edit_message_text(
            f"Messages: {info.get('messages', 0)}\n"
            f"First seen: {info.get('since', '?')}"
        )


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Error:", exc_info=context.error)


# --- Main ---

def main():
    print("Bot starting...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("jump", jump))
    app.add_handler(CommandHandler("channels", channels))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("echo", echo))
    app.add_handler(CommandHandler("time", time_cmd))

    app.add_handler(CallbackQueryHandler(on_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    app.add_error_handler(on_error)

    print("Polling...")
    app.run_polling(poll_interval=3)


if __name__ == "__main__":
    main()

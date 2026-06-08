import os
import logging
from dotenv import load_dotenv
from google import genai

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in .env file")

if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY in .env file")

client = genai.Client(api_key=GEMINI_API_KEY)

logging.basicConfig(level=logging.INFO)

SYSTEM_INSTRUCTIONS = """
Answer with only the final answer.

Rules:
- No introductions
- No explanations
- No headings
- No markdown
- No reasoning
- No 'Task Understanding'
- No 'Actions Taken'
- No 'Result'
- No 'Suggested Next Steps'

For calculations, return only the number.
For factual questions, return only the answer.
Keep responses as short as possible.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey! I’m your AI Agent Manager on Telegram.\n\nSend me a task."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text or ""
    chat_id = update.effective_chat.id

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        prompt = SYSTEM_INSTRUCTIONS + "\n\nUser request:\n" + user_text

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        answer = response.text or "I could not generate a response."

        for i in range(0, len(answer), 3900):
            await update.message.reply_text(answer[i:i + 3900])

    except Exception as e:
        logging.exception("Gemini request failed")
        await update.message.reply_text(f"Sorry, something went wrong:\n\n{e}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Telegram Gemini AI Agent is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
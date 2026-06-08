# Telegram AI Agent MVP

This is a minimal Telegram AI Agent Manager.

## What it does

Telegram user message → Python bot → OpenAI Responses API → Telegram reply.

## 1. Create Telegram bot

Open Telegram and message `@BotFather`.

Run:

```text
/newbot
```

Follow the steps and copy the bot token.

## 2. Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configure secrets

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Then add:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5.5
```

## 4. Run

```bash
python bot.py
```

Open your bot in Telegram and send:

```text
/start
```

## 5. Production idea

For production, deploy it to a VPS or Render/Railway/Fly.io and switch from long polling to webhooks.

## Next improvements

- Add SQLite/Postgres memory
- Add user permissions
- Add file upload handling
- Add image handling
- Add tool routing
- Add web search
- Add admin dashboard

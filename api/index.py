import os
import asyncio
from fastapi import FastAPI, Request, Header, BackgroundTasks
from telegram import Update
from telegram.ext import Application

from bot_app import build_application

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("Missing TELEGRAM_TOKEN in Vercel Environment Variables")

WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET", "")

app = FastAPI()

_ptb_app: Application | None = None
_inited = False
_lock = asyncio.Lock()

async def _ensure_ptb() -> Application:
    global _ptb_app, _inited
    async with _lock:
        if _ptb_app is None:
            _ptb_app = build_application(TELEGRAM_TOKEN)
        if not _inited:
            await _ptb_app.initialize()
            _inited = True
    return _ptb_app

# health check
@app.get("/")
async def health():
    return {"ok": True}

# Telegram will call https://DOMAIN/api/webhook
@app.post("/webhook")
async def telegram_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    if WEBHOOK_SECRET and x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
        return {"ok": True}

    data = await request.json()
    ptb = await _ensure_ptb()

    background_tasks.add_task(_process_update, ptb, data)
    return {"ok": True}

async def _process_update(ptb: Application, data: dict):
    update = Update.de_json(data, ptb.bot)
    await ptb.process_update(update)

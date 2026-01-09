import os
import asyncio
from fastapi import FastAPI, Request, Header
from telegram import Update
from telegram.ext import Application

from bot_app import build_application

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
WEBHOOK_SECRET = os.environ.get("TELEGRAM_WEBHOOK_SECRET", "")

app = FastAPI()  # ini WAJIB top-level dan namanya "app"

_ptb_app: Application | None = None
_started = False
_lock = asyncio.Lock()

async def _ensure_ptb():
    global _ptb_app, _started
    async with _lock:
        if _ptb_app is None:
            _ptb_app = build_application(TELEGRAM_TOKEN)
        if not _started:
            await _ptb_app.initialize()
            await _ptb_app.start()
            _started = True
    return _ptb_app

@app.get("/")
async def health():
    return {"ok": True}

@app.post("/")
async def webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    if WEBHOOK_SECRET and x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
        return {"ok": True}

    data = await request.json()
    ptb = await _ensure_ptb()

    update = Update.de_json(data, ptb.bot)
    await ptb.process_update(update)
    return {"ok": True}

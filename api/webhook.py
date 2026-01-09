import os
import asyncio
from fastapi import FastAPI, Request, Header
from telegram import Update
from telegram.ext import Application

from bot_app import build_application

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
WEBHOOK_SECRET = os.environ.get("TELEGRAM_WEBHOOK_SECRET", "")

_ptb_app: Application | None = None
_ptb_started: bool = False
_lock = asyncio.Lock()

async def _get_ptb_app() -> Application:
    global _ptb_app, _ptb_started
    async with _lock:
        if _ptb_app is None:
            _ptb_app = build_application(TELEGRAM_TOKEN)

        if not _ptb_started:
            await _ptb_app.initialize()
            await _ptb_app.start()
            _ptb_started = True

        return _ptb_app

app = FastAPI()

@app.get("/")
async def health():
    return {"ok": True}

@app.post("/")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    if WEBHOOK_SECRET:
        if x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
            return {"ok": True}

    data = await request.json()
    ptb = await _get_ptb_app()

    update = Update.de_json(data, ptb.bot)
    await ptb.process_update(update)

    return {"ok": True}

import logging
import os
import asyncio
from dotenv import load_dotenv

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

import google.generativeai as genai

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"

SYSTEM_MESSAGE = """
Kamu adalah DJerukBot 🤖🌿 asisten informasi Desa Jeruk, Pacitan.
Aturan:
- ubah agar respon di instagram sesuai dengan format telegram dan bukan GPT seperti:
- Jangan gunakan markdown bullet seperti * atau -
- Gunakan bullet unicode • untuk daftar
- Jangan gunakan **bold** atau _italic_
- Gunakan paragraf singkat dan bullet •
- Maksimal 8 bullet per jawaban
- Gunakan Bahasa Indonesia atau Bahasa Jawa mengikuti bahasa user.
- Gunakan emoticon yang ramah tapi tetap profesional 🙂🙏✅📌📍
- Jawaban ringkas, jelas, rapi.
- Jika tidak tahu atau tidak yakin, katakan jujur dan minta user memperjelas.
- Jangan minta data sensitif seperti NIK lengkap, OTP, password, rekening.
- Buat jawaban dengan singkat padat dan jelas, jangan buat panjang lebar.
- untuk informasi seputar desa jeruk anda dapat melihat lewawt "wikipedia" atau web resmi desa jeruk di "desajeruk.id"
""".strip()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Halo, aku DJerukBot 🤖🌿\n"
        "Kamu bisa tanya apa saja seputar Desa Jeruk atau pertanyaan umum juga ya 🙂✅"
    )
    await update.message.reply_text(text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = (update.message.text or "").strip()
    if not user_text:
        return

    await update.message.chat.send_action(ChatAction.TYPING)
    processing = await update.message.reply_text("Djeruk sedang berpikir, mohon tunggu... ⏳🙂")

    try:
        response = await get_gemini_response(user_text)

        try:
            await processing.delete()
        except Exception:
            pass

        await update.message.reply_text(response)

    except asyncio.TimeoutError:
        try:
            await processing.delete()
        except Exception:
            pass
        await update.message.reply_text(
            "Maaf ya, JerukBot kehabisan waktu saat memproses jawaban 😅\n"
            "Coba kirim ulang pertanyaanmu ya 🙂🙏"
        )
    except Exception:
        logger.exception("handle_message error")
        try:
            await processing.delete()
        except Exception:
            pass
        await update.message.reply_text(
            "Maaf ya, JerukBot lagi error 😅🔧\n"
            "Coba lagi sebentar ya 🙂🙏"
        )


async def get_gemini_response(query: str) -> str:
    if not GEMINI_API_KEY:
        return "API key Gemini belum diset di Environment Variables ya 🙂🙏"

    model = genai.GenerativeModel(MODEL_NAME)
    prompt = f"{SYSTEM_MESSAGE}\n\nPertanyaan pengguna:\n{query}"

    def _call_gemini():
        return model.generate_content(
            prompt,
            request_options={"timeout": 20}
        )

    result = await asyncio.wait_for(asyncio.to_thread(_call_gemini), timeout=25)

    text = (getattr(result, "text", None) or "").strip()
    if not text:
        return "Maaf ya, JerukBot tidak mendapat jawaban dari Gemini 😅🙏"

    return text


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Update caused error: %s", context.error)


def build_application(token: str) -> Application:
    app = (
        Application.builder()
        .token(token)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .pool_timeout(30)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    return app

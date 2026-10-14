import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatAction
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("translator-bot")

TRANSLATE_CHUNK = 4500  # bitta tarjima so'rovi uchun maksimal uzunlik
MESSAGE_CHUNK = 4000    # bitta Telegram xabari uchun maksimal uzunlik

START_TEXT = (
    "Assalomu alaykum! 👋 Men o'zbekchadan ruschaga tarjima qilaman. "
    "✍️ Matn yozing — ruscha tarjimasini qaytaraman."
)
ONLY_TEXT = "✍️ Iltimos, o'zbekcha matn yuboring."
ERROR_TEXT = "❌ Xatolik yuz berdi. Birozdan keyin qayta urinib ko'ring."

dp = Dispatcher()


def split_text(text: str, limit: int) -> list[str]:
    """Matnni `limit` dan oshmaydigan bo'laklarga bo'ladi.

    Iloji boricha qator, gap yoki bo'shliq chegarasida kesadi.
    """
    chunks: list[str] = []
    rest = text
    while len(rest) > limit:
        window = rest[:limit]
        cut = -1
        for sep in ("\n", ". ", "! ", "? ", " "):
            pos = window.rfind(sep)
            if pos > limit // 2:
                cut = pos + len(sep)
                break
        if cut == -1:
            cut = limit
        chunks.append(rest[:cut])
        rest = rest[cut:]
    if rest:
        chunks.append(rest)
    return [c for c in chunks if c.strip()]


def translate_sync(text: str) -> str:
    """Sinxron tarjima (uz -> ru), uzun matnni bo'laklab tarjima qiladi."""
    translator = GoogleTranslator(source="uz", target="ru")
    result = ""
    for chunk in split_text(text, TRANSLATE_CHUNK):
        translated = (translator.translate(chunk) or "").strip()
        if translated:
            # bo'lak qator oxirida kesilgan bo'lsa, qatorni saqlaymiz
            result += translated + ("\n" if chunk.endswith("\n") else " ")
    return result.strip()


async def translate(text: str) -> str:
    """Event loop qotib qolmasligi uchun tarjimani alohida oqimda bajaradi."""
    return await asyncio.to_thread(translate_sync, text)


@dp.message(CommandStart())
async def on_start(message: Message) -> None:
    await message.answer(START_TEXT)


@dp.message(F.text)
async def on_text(message: Message, bot: Bot) -> None:
    try:
        async with ChatActionSender(
            bot=bot, chat_id=message.chat.id, action=ChatAction.TYPING
        ):
            result = await translate(message.text)
        if not result:
            raise ValueError("Bo'sh tarjima qaytdi")
        for part in split_text(result, MESSAGE_CHUNK):
            await message.answer(part)
    except Exception:
        log.exception("Tarjima xatosi (chat_id=%s)", message.chat.id)
        await message.answer(ERROR_TEXT)


@dp.message()
async def on_other(message: Message) -> None:
    await message.answer(ONLY_TEXT)


@dp.errors()
async def on_error(event) -> bool:
    log.error("Kutilmagan xato: %s", event.exception, exc_info=event.exception)
    return True


async def main() -> None:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token or token.startswith("<"):
        log.error("BOT_TOKEN topilmadi. .env faylga yoki muhit o'zgaruvchisiga qo'shing.")
        sys.exit(1)

    bot = Bot(token=token)
    try:
        me = await bot.get_me()
        log.info("Bot ishga tushdi: @%s", me.username)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("Bot to'xtatildi")

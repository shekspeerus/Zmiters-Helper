from telegram import Update
from telegram.ext import ContextTypes

from core.i18n import get_current_lang, set_lang, get_texts


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    current = get_current_lang(context)
    new_lang = "ru" if current == "by" else "by"
    set_lang(context, new_lang)
    texts = get_texts(context)
    await update.message.reply_text(texts.START_MESSAGE)



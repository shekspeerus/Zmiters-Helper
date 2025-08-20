from telegram import Update
from telegram.ext import ContextTypes
from core.i18n import get_texts


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	texts = get_texts(context)
	await update.message.reply_text(texts.ABOUT_MESSAGE)




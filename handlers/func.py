import logging
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, getcontext
from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from core.i18n import get_texts


logger = logging.getLogger(__name__)


AWAITING_A, AWAITING_B, AWAITING_Y = range(3)


getcontext().prec = 28


def parse_user_input_number(text: str) -> Decimal:
    normalized = text.replace(',', '.').strip()
    return Decimal(normalized)


def count_fractional_digits(text: str) -> int:
    normalized = text.replace(',', '.').strip()
    if '.' in normalized:
        return len(normalized.split('.', 1)[1])
    return 0


async def func_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    texts = get_texts(context)
    await update.message.reply_text(texts.FUNC_START)
    return AWAITING_A


async def get_a(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        a = parse_user_input_number(update.message.text)
        context.user_data["a"] = a
        context.user_data["a_places"] = count_fractional_digits(update.message.text)
        texts = get_texts(context)
        await update.message.reply_text(texts.FUNC_ASK_B)
        return AWAITING_B
    except (ValueError, InvalidOperation):
        texts = get_texts(context)
        await update.message.reply_text(texts.FUNC_ERROR_NUMBERS)
        return AWAITING_A


async def get_b(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        b = parse_user_input_number(update.message.text)
        context.user_data["b"] = b
        context.user_data["b_places"] = count_fractional_digits(update.message.text)
        texts = get_texts(context)
        await update.message.reply_text(texts.FUNC_ASK_Y)
        return AWAITING_Y
    except (ValueError, InvalidOperation):
        texts = get_texts(context)
        await update.message.reply_text(texts.FUNC_ERROR_NUMBERS)
        return AWAITING_B


async def get_y(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        y = parse_user_input_number(update.message.text)
        context.user_data["y_places"] = count_fractional_digits(update.message.text)
        a: Decimal = context.user_data["a"]
        b: Decimal = context.user_data["b"]

        result: Decimal = a + b - y

        a_places = int(context.user_data.get("a_places", 0))
        b_places = int(context.user_data.get("b_places", 0))
        y_places = int(context.user_data.get("y_places", 0))
        max_places = max(a_places, b_places, y_places)
        quant = Decimal(1).scaleb(-max_places) if max_places > 0 else Decimal(1)
        rounded_result = result.quantize(quant, rounding=ROUND_HALF_UP)

        texts = get_texts(context)
        await update.message.reply_text(
            texts.FUNC_SUCCESS.format(a=a, b=b, y=y, result=rounded_result)
        )

        return ConversationHandler.END

    except (ValueError, InvalidOperation):
        texts = get_texts(context)
        await update.message.reply_text(texts.FUNC_ERROR_NUMBERS)
        return AWAITING_Y
    except Exception as e:
        texts = get_texts(context)
        logger.error(texts.FUNC_ERROR_LOG.format(e))
        await update.message.reply_text(texts.FUNC_GENERAL_ERROR)
        context.user_data.clear()
        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    texts = get_texts(context)
    await update.message.reply_text(texts.FUNC_CANCELLED)
    return ConversationHandler.END


async def repeat_with_previous(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if "a" in context.user_data and "b" in context.user_data:
        texts = get_texts(context)
        await update.message.reply_text(texts.FUNC_ASK_Y)
        return AWAITING_Y
    texts = get_texts(context)
    await update.message.reply_text(texts.REPEAT_NO_STATE)
    return ConversationHandler.END


def build_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            CommandHandler("func", func_start),
            CommandHandler("repeat", repeat_with_previous),
        ],
        states={
            AWAITING_A: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_a)],
            AWAITING_B: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_b)],
            AWAITING_Y: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_y)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )



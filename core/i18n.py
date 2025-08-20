from telegram.ext import ContextTypes

from locales import by as texts_by
from locales import ru as texts_ru


DEFAULT_LANG = "by"
SUPPORTED_LANGS = {"by": texts_by, "ru": texts_ru}


def get_current_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    lang = context.user_data.get("lang")
    if lang in SUPPORTED_LANGS:
        return lang
    return DEFAULT_LANG


def set_lang(context: ContextTypes.DEFAULT_TYPE, lang: str) -> None:
    if lang in SUPPORTED_LANGS:
        context.user_data["lang"] = lang


def get_texts(context: ContextTypes.DEFAULT_TYPE):
    lang = get_current_lang(context)
    return SUPPORTED_LANGS[lang]



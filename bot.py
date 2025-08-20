import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler

from commands import post_init
from handlers import start, build_conversation_handler, language, about


load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not token:
        logger.error("не знойдзены токен бота! стварыце файл .env з TELEGRAM_BOT_TOKEN=ваш_токен")
        return

    application = Application.builder().token(token).build()

    application.post_init = post_init

    application.add_handler(CommandHandler("start", start))
    application.add_handler(build_conversation_handler())
    application.add_handler(CommandHandler("language", language))
    application.add_handler(CommandHandler("about", about))

    logger.info("бот запушчаны...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()



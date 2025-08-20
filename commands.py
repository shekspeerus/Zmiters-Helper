import logging
from telegram import BotCommand
from telegram.ext import Application

from locales.by import COMMAND_DESCRIPTIONS


logger = logging.getLogger(__name__)


async def set_commands(application: Application) -> None:
    commands = [
        BotCommand(command, description) for command, description in COMMAND_DESCRIPTIONS
    ]
    await application.bot.set_my_commands(commands)
    logger.info("меню каманд усталявана.")


async def post_init(application: Application) -> None:
    await set_commands(application)



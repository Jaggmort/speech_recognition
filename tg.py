import os
import logging

import dialog_flow
import dotenv
import telegram

from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from telegram_log import TelegramLogsHandler


logger = logging.getLogger(__name__)


def answer(update: Update, context: CallbackContext) -> None:
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    telegram_user_id = os.getenv('TELEGRAM_CHAT_ID')
    msg, is_fallback = dialog_flow.detect_intent_texts(
        project_id,
        telegram_user_id,
        update.message.text,
        'ru'
        )
    update.message.reply_text(msg)


def main() -> None:
    dotenv.load_dotenv('.env')
    tg_token = os.environ['TELEGRAM_TOKEN']
    tg_announce_token = os.environ['TG_ANNOUNCE_TOKEN']
    tg_announce_bot = telegram.Bot(tg_announce_token)
    tg_announce_id = os.environ['TELEGRAM_USER_ID']

    logger_settings = TelegramLogsHandler(tg_announce_bot, tg_announce_id)
    logger_settings.setLevel(logging.INFO)
    logger_settings.setFormatter(
        logging.Formatter("%(asctime)s: %(levelname)s; %(message)s")
        )
    logger.addHandler(logger_settings)

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, answer)
        )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

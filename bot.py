import os

import dialog_flow
import dotenv
import logging

from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def answer(update: Update, context: CallbackContext) -> None:
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    telegram_user_id = os.getenv('TELEGRAM_CHAT_ID')
    msg, _ = dialog_flow.detect_intent_texts(
        project_id,
        telegram_user_id,
        update.message.text,
        'ru'
        )
    update.message.reply_text(msg)


def main() -> None:
    dotenv.load_dotenv('.env')
    tg_token = os.environ['TELEGRAM_TOKEN']
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, answer)
        )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

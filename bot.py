import os

import dotenv
import logging

from google.cloud import dialogflow
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def answer(update: Update, context: CallbackContext) -> None:
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    telegram_user_id = os.getenv('TELEGRAM_CHAT_ID')
    msg, _ = detect_intent_texts(
        project_id,
        telegram_user_id,
        update.message.text,
        'ru'
        )
    update.message.reply_text(msg)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    intent_text = response.query_result.fulfillment_text
    is_fallback = response.query_result.intent.is_fallback
    return intent_text, is_fallback


def main() -> None:
    dotenv.load_dotenv('.env')
    tg_token = os.environ['TELEGRAM_TOKEN']
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

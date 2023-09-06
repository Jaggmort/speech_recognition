import logging
import os
import random

import dialog_flow
import telegram
import urllib
import vk_api

from dotenv import load_dotenv
from telegram_log import TelegramLogsHandler
from vk_api.longpoll import VkLongPoll, VkEventType


logger = logging.getLogger(__name__)


def answer(event, vk_session, project_id):
    intent_text, is_fallback = dialog_flow.detect_intent_texts(
        project_id,
        event.user_id,
        event.text,
        'ru'
        )
    if not is_fallback:
        vk_session.method(
            'messages.send',
            {'user_id': event.user_id,
             'message': intent_text,
             'random_id': random.randint(1, 1000)}
             )


def main():
    load_dotenv()
    vk_chat_token = os.getenv('VK_CHAT_TOKEN')
    vk_session = vk_api.VkApi(token=vk_chat_token)
    longpoll = VkLongPoll(vk_session)

    tg_announce_token = os.environ['TG_ANNOUNCE_TOKEN']
    tg_announce_bot = telegram.Bot(tg_announce_token)
    tg_announce_id = os.environ['TELEGRAM_USER_ID']
    logger_settings = TelegramLogsHandler(tg_announce_bot, tg_announce_id)
    logger_settings.setLevel(logging.INFO)
    logger_settings.setFormatter(
        logging.Formatter("%(asctime)s: %(levelname)s; %(message)s")
        )
    logger.addHandler(logger_settings)

    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                answer(event, vk_session, project_id)
            except urllib.error.HTTPError as error:
                logger.error(f'VK-бот упал с ошибкой: {error} {error.url}')
            except Exception as error:
                logger.error(f'VK-бот упал с ошибкой: {error}')


if __name__ == '__main__':
    main()

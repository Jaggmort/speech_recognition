import os

import dialog_flow
import logging
import vk_api
import urllib

from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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
             'random_id': 0}
             )


def main():
    load_dotenv()
    vk_chat_token = os.getenv('VK_CHAT_TOKEN')
    vk_session = vk_api.VkApi(token=vk_chat_token)
    longpoll = VkLongPoll(vk_session)

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

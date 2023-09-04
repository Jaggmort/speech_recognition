import os

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv


def main()
    load_dotenv()
    vk_chat_token = os.getenv('VK_CHAT_TOKEN')
    vk_session = vk_api.VkApi(token=vk_chat_token)

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
                id = event.chat_id
                vk_session.method('messages.send', {'chat_id': id, 'message': event.text, 'random_id': 0})
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


if __name__ == '__main__':
    main()

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token="vk1.a.I5vL60r5VSgl8JWBZYvHQSDAstzs8bMtjNAAqGYhcGyi6iVRVmy0A1JpNWqaKgSz9TpDOhR_hc91KGQTTtAX_MXBGVlqDo_Fw-INVZwV4RpKKzv9iZsgNe-k-dZCtGJXCZNc86VSRnIn48RyH9PKo9IVTz7lEdJnV1XrSLqEKWq02u3cu7ZXVLjLzOrIh8s8RCFml0ixumSdBD7TAsQCgQ")

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

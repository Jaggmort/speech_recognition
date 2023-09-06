# speech_recognition
 
## Переменные окружения

Часть настроек проекта берётся из переменных окружения.  
Чтобы их определить, создайте файл `.env` рядом с `bot.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ = значение`:  

- `TELEGRAM_TOKEN` — Токен вашего бота, который вы будете использовать для оповещения.  
- `TELEGRAM_CHAT_ID` — Ваш Telegram_id, на который бот будет отсылать сообщения.
- `GOOGLE_CLOUD_PROJECT` - Project ID проекта в Google Cloud , привязанного к DialogFlow [Как получить](https://cloud.google.com/dialogflow/es/docs/quick/setup)
- `GOOGLE_APPLICATION_CREDENTIALS` — Путь к credentials.json.
- `VK_CHAT_TOKEN` - Токен вк, необходим для взаимодействия через вк.
- `TG_ANNOUNCE_TOKEN` - Токен телеграм бота, для отслеживания ошибок.
- `TELEGRAM_USER_ID` - ID пользователя телеграм, которому будут отсылаться ошибки.


## Установка и запуск
Для запуска у вас уже должен быть установлен Python не ниже 3-й версии.  

- Скачайте код
- Создайте и заполните файл с переменными окружения, активируйте виртуальное окружение: `python -m venv venv`
- Windows: `.\venv\Scripts\activate`
- Установите зависимости командой `pip install -r requirements.txt`
- Запустите ботов - командой `python tg.py` / `python vk.py`

## Добавьте информацию для DialogFlow

В корневой дирректории создайте файл  questions.json, содержащий подготовленные вопросы и ответы.
Пример:
`
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
    ...
}
`

- Запустите скрипт `python dialog_flow.py questions.json`
- Запустите бота тг `python tg.py`
- Запустите бота вк `python vk.py`

Пример диалога:

![Пример](C:\Work_py\speech_ex.png)

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).

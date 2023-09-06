import argparse
import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


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


def create_intent(
        project_id,
        display_name,
        training_phrases_parts,
        message_texts
        ):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
            )
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent, "language_code": "ru", }
    )

    print("Intent created: {}".format(response))


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description='Скрипт для заполенения DialogFlow вопросами и ожидаемыми ответами'
    )
    parser.add_argument(
        'file_name',
        nargs='?',
        default='questions.json',
        help='Подготовленный .json - файл'
    )
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    with open(parser.parse_args().file_name, "r", encoding="UTF-8") as questions_file:
        questions_array = json.loads(questions_file.read())
    for question_subject, questions in questions_array.items():
        create_intent(
            project_id,
            question_subject,
            questions['questions'],
            [questions['answer']]
            )


if __name__ == '__main__':
    main()

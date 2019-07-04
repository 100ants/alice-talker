# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
import eliza

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и спросим его о здоровье

        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ],
            'elizabot': eliza.eliza()
        }

        res['response']['text'] = 'Hello.  How are you feeling today?'
        return

    # Если нет, то продолжим беседу
    res['response']['text'] = sessionStorage[user_id]['elizabot'].respond(req['request']['original_utterance'])
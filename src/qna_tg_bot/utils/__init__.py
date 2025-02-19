import json
import os

from qna_tg_bot.config import BASE_DIR

def load_qna_map():
    with open(os.path.join(BASE_DIR, 'data/qna.json'), 'r', encoding='utf-8') as file:
        return json.load(file)

def find_answer(user_input: str) -> str:
    user_input = user_input.lower()
    qna_map = load_qna_map()
    for question, answer in qna_map.items():
        if user_input in question.lower():
            return f'<b>Вопрос</b>\n«{question}»\n<b>Ответ</b>\n{answer}'
    return 'Ответ не найден... кажется бот слишком тупой...'

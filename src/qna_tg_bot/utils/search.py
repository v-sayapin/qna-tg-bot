import json
import os
import re
from collections import defaultdict
from functools import lru_cache
from rapidfuzz import process

from qna_tg_bot.config import BASE_DIR

DEFAULT_QUESTION_SCORE_THRESHOLD = 50
DEFAULT_WORD_SCORE_THRESHOLD = 65
WORD_PATTERN = re.compile(r'\w+')

@lru_cache(maxsize=1)
def _load_qna_data() -> dict:
    with open(os.path.join(BASE_DIR, 'data/qna.json'), 'r', encoding='utf-8') as file:
        qna_map = json.load(file)

    word_index = defaultdict(set)
    questions_lower = []

    for question in qna_map:
        question_lower = question.lower()
        questions_lower.append(question_lower)

        words = WORD_PATTERN.findall(question_lower)
        for word in words:
            word_index[word].add(question)

    return {
        'qna_map': qna_map,
        'questions_lower': questions_lower,
        'word_index': word_index,
        'unique_words': list(word_index.keys())
    }

def _preprocess_input(query: str) -> list[str]:
    return WORD_PATTERN.findall(query.lower())

def _search_candidates(query_words: list[str], word_index: dict[str, set[str]], unique_words: list[str]) -> set[str]:
    candidates = set()

    for word in query_words:
        similar_words = process.extract(word, unique_words, score_cutoff=DEFAULT_WORD_SCORE_THRESHOLD, limit=10)
        for similar_word, _, _ in similar_words:
            candidates.update(word_index.get(similar_word, set()))

    return candidates

def _search_best_match(query_lower: str, candidate_questions_lower: list[str], candidate_questions: list[str], qna_map: dict[str, str]) -> str | None:
    best_match = process.extractOne(query_lower, candidate_questions_lower, score_cutoff=DEFAULT_QUESTION_SCORE_THRESHOLD)
    if not best_match:
        return None

    index = candidate_questions_lower.index(best_match[0])
    question = candidate_questions[index]
    answer = qna_map[question]
    return _format_answer(question, answer)

def _search_best_match_in_all(query_lower: str, qna_data: dict[str, any]) -> str | None:
    best_match = process.extractOne(query_lower, qna_data['questions_lower'], score_cutoff=DEFAULT_QUESTION_SCORE_THRESHOLD)
    if not best_match:
        return None

    index = qna_data['questions_lower'].index(best_match[0])
    question = list(qna_data['qna_map'].keys())[index]
    answer = qna_data['qna_map'][question]
    return _format_answer(question, answer)

def _format_answer(question: str, answer: str) -> str:
    return f'<b>Вопрос</b>\n«{question}»\n<b>Ответ</b>\n{answer}'

def _not_found_answer() -> str:
    return 'Ответ не найден...'

def search_answer_by_query(query: str) -> str:
    query_lower = query.lower()
    qna_data = _load_qna_data()

    query_words = _preprocess_input(query)
    candidates = _search_candidates(query_words, qna_data['word_index'], qna_data['unique_words'])

    if candidates:
        candidate_questions = list(candidates)
        candidate_questions_lower = [q.lower() for q in candidate_questions]
        best_match = _search_best_match(query_lower, candidate_questions_lower, candidate_questions, qna_data['qna_map'])
        if best_match:
            return best_match

    best_match = _search_best_match_in_all(query_lower, qna_data)
    return best_match if best_match else _not_found_answer()

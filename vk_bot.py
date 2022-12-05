import os
import random
import logging

from dotenv import load_dotenv

import redis

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from get_quiz import get_questions_and_answers_from_file


logger = logging.getLogger("quizbot")

def start_quiz(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message="Привет! Я бот для викторин!",
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard()
    )


def send_question(event, vk_api, redis_db, quiz):
    question = random.choice(list(quiz.keys()))
    user_id = event.user_id
    vk_api.messages.send(
        user_id=user_id,
        message=question,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard()
    )
    redis_db.set(user_id, question)


def check_answer(event, vk_api, redis_db):
    user_id = event.user_id
    redis_get = redis_db.get(user_id)
    buttons = ["старт", "новый вопрос", "сдаться", "мой счет"]
    if event.text.lower() not in buttons:
        answer = [
                answer.strip(".").lower() for answer in quiz[redis_get].split("\n")
        ]
        logger.info(answer)
        if event.text in answer:
            vk_api.messages.send(
                user_id=user_id,
                message="Все правильно, молодец!",
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
        if event.text not in answer:
            vk_api.messages.send(
                user_id=user_id,
                message="Попробуй еще!",
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )


def handle_surrend(event, vk_api, redis_db, quiz):
    user_id = event.user_id
    question = redis_db.get(user_id)
    logger.info(question)
    logger.info(quiz)
    answer = quiz[question] 
    vk_api.messages.send(
        user_id=user_id,
        message=answer,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard()
    )
    question = random.choice(list(quiz.keys()))
    vk_api.messages.send(
        user_id=user_id,
        message=question,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard()
    )
    redis_db.set(user_id, question)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    load_dotenv()
    quiz = get_questions_and_answers_from_file("120br2.txt")
    redis_db = redis.Redis(
        host=os.getenv("REDIS_DB"),
        port=os.getenv("REDIS_PORT"),
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
    )
    vk_session = vk_api.VkApi(token=os.getenv("VK_BOT_TOKEN"))
    vk_api = vk_session.get_api()
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Новый вопрос", VkKeyboardColor.POSITIVE)
    keyboard.add_button("Сдаться", VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button("Мой счет")
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            check_answer(event, vk_api, redis_db)
            if event.text == "Старт":
                start_quiz(event, vk_api)
            if event.text == "Новый вопрос":
                send_question(event, vk_api, redis_db, quiz)
            if event.text == "Сдаться":
                handle_surrend(event, vk_api, redis_db, quiz)

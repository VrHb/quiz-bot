import argparse
from enum import IntEnum
import random
import os
import logging
from functools import partial

from dotenv import load_dotenv
import redis

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    ConversationHandler, RegexHandler

from get_quiz import get_questions_and_answers_from_file


logger = logging.getLogger("quizbot")

class Stage(IntEnum):
    QUESTION = 1
    ANSWER = 2

quiz_keyboard = [["Новый вопрос", "Сдаться"], ["Мой счет"]]
reply_markup = ReplyKeyboardMarkup(quiz_keyboard)


def start_quiz(bot, update):
    chat_id = update.message.from_user.id
    bot.send_message(
        chat_id=chat_id,
        text="Привет! Я бот для викторин!",
        reply_markup=reply_markup
    )
    return Stage.QUESTION


def handle_new_question_request(bot, update, redis, quiz):
    user_id = update.message.from_user.id
    question = random.choice(list(quiz.keys()))
    bot.send_message(
        chat_id=user_id,
        text=question,
        reply_markup=reply_markup
    )
    redis_set = redis.set(user_id, question)
    logger.info(redis_set)
    return Stage.ANSWER


def handle_solution_attempt(bot, update, redis, quiz):
    user_id = update.message.from_user.id
    question = redis.get(user_id)
    logger.info(question)
    answer = [
        answer.strip(".").lower() for answer in quiz[question].split("\n")
    ]
    logger.info(answer)
    if update.message.text.lower() in answer:
        bot.send_message(
            chat_id=user_id,
            text="Правильно! Поздравляю!",
            reply_markup=reply_markup
        )
        return Stage.QUESTION
    if update.message.text.lower() not in answer:
        bot.send_message(
            chat_id=user_id,
            text="Неправильно... Попробуешь еще раз?",
            reply_markup=reply_markup
        )
        return Stage.ANSWER


def handle_surrend(bot, update, redis, quiz):
    user_id = update.message.from_user.id
    question = redis.get(user_id)
    logger.info(question)
    answer = quiz[question] 
    bot.send_message(
        chat_id=user_id,
        text=answer,
    )
    question = random.choice(list(quiz.keys()))
    bot.send_message(
        chat_id=user_id,
        text=question,
    )
    redis_set = redis.set(user_id, question)
    logger.info(redis_set)
    return Stage.ANSWER


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Бот для проведения викторины.")
    parser.add_argument(
        "--path",
        default="./quiz-questions",
        help="Путь к директории с квизами"
    )
    parser.add_argument(
        "--filename",
        default="120br2.txt",
        help="Имя файла"
    )
    args = parser.parse_args()
    quiz = get_questions_and_answers_from_file(args.path, args.filename)
    redis_db = redis.Redis(
        host=os.getenv("REDIS_DB"),
        port=os.getenv("REDIS_PORT"),
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
    )
    updater = Updater(os.getenv("TG_BOT_TOKEN"))
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_quiz)],

        states={
            Stage.QUESTION: [
                RegexHandler("^(Новый вопрос)$",
                    partial(handle_new_question_request, redis=redis_db, quiz=quiz))
            ],
            Stage.ANSWER: [
                RegexHandler("^(Сдаться)$",
                    partial(handle_surrend, redis=redis_db, quiz=quiz)),
                RegexHandler("^(Новый вопрос)$",
                    partial(handle_new_question_request, redis=redis_db, quiz=quiz)),
                MessageHandler(Filters.text, 
                    partial(handle_solution_attempt, redis=redis_db, quiz=quiz)),
            ],

        },
        fallbacks=[]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    main()

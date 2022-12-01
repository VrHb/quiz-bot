import os
import logging

from dotenv import load_dotenv

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


quiz_keyboard = [["Новый вопрос", "Сдаться"], ["Мой счет"]]
reply_markup = ReplyKeyboardMarkup(quiz_keyboard)

def echo(bot, update):
    chat_id = update.message.from_user.id
    bot.send_message(
        chat_id=chat_id,
        text=update.message.text,
        reply_markup=reply_markup
    )


def main():
    load_dotenv()
    updater = Updater(os.getenv("TG_BOT_TOKEN"))
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    logger = logging.getLogger("quizbot")
    main()

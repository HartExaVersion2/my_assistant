import telebot
import os
from common.logger import Log
from common.errors import UnknownError

token = os.environ.get("TelegramToken")
user_id = os.environ.get("PrilepskiyTelegramId")

logger = Log('assistant_bot', 'Bot/assistant_bot.py', 'assistant_bot')
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.reply_to(message, "Привет! Я Активирован")
    except Exception as error:
        message = 'function {} error {}'.format(start.__name__, error)
        logger.error(message)
        raise UnknownError
def send_message_to_user(message_text):
    try:
        bot.send_message(user_id, message_text)
    except Exception as error:
        message = 'function {} error {}'.format(send_message_to_user.__name__, error)
        logger.error(message)
        raise UnknownError
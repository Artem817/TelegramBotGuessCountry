import json
import random
import logging
import telebot
from telebot import types

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def load_countries():
    try:
        with open('countries.json', 'r', encoding='utf-8') as f:
            countries = json.load(f)
        return countries
    except FileNotFoundError:
        logger.error("Файл countries.json не знайдено. Сформуйте файл за допомогою генератора.")
        return []

countries = load_countries()
if not countries:
    logger.error("Не вдалося завантажити дані країн. Перевірте наявність файлу countries.json.")

user_data = {}

TOKEN = 'token'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_game(message):
    if not countries:
        bot.send_message(message.chat.id, "На жаль, неможливо завантажити дані країн. Спробуйте пізніше.")
        return
    bot.send_message(
        message.chat.id,
        "Гра Вгадай столицю починається. Я назву країну, а ти вибери правильну столицю.",
        reply_markup=main_keyboard()
    )
    send_question(message.chat.id)

def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Показати відповідь"))
    keyboard.add(types.KeyboardButton("Зупинити гру"))
    return keyboard

def send_question(chat_id):
    country = random.choice(countries)
    correct_capital = country['capital']
    wrong_capitals = random.sample(
        [c['capital'] for c in countries if c['capital'] != correct_capital],
        3
    )
    options = wrong_capitals + [correct_capital]
    random.shuffle(options)
    user_data[chat_id] = {'country': country['country'], 'capital': correct_capital}
    question = f"Яка столиця країни **{country['country']}**?"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for option in options:
        markup.add(types.KeyboardButton(option))
    bot.send_message(chat_id, question, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text

    if chat_id not in user_data:
        bot.send_message(chat_id, "Будь ласка, розпочніть гру командою /start.")
        return

    if text == "Показати відповідь":
        correct = user_data[chat_id]['capital']
        bot.send_message(chat_id, f"Правильна відповідь: {correct}", reply_markup=main_keyboard())
        send_question(chat_id)
        return

    if text == "Зупинити гру":
        bot.send_message(chat_id, "Гра зупинена. Дякую за гру!", reply_markup=types.ReplyKeyboardRemove())
        del user_data[chat_id]
        return

    correct = user_data[chat_id]['capital']
    if text.lower() == correct.lower():
        bot.send_message(chat_id, "Правильно! Молодець!", reply_markup=main_keyboard())
        send_question(chat_id)
    else:
        bot.send_message(chat_id, f"Неправильно. Спробуй ще раз або натисни 'Показати відповідь'.", reply_markup=main_keyboard())

if __name__ == '__main__':
    bot.polling(none_stop=True)

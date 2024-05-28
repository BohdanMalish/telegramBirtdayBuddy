import os
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привіт! Я бот, який може генерувати привітання з днем народження. Використовуйте команду /birthday <ім'я> <вік> <хобі>, щоб отримати привітання.")


def generate_birthday_greeting(name, age, hobby):
    prompt = f"Напиши привітання з днем народження для {name}, якому виповнюється {age} років, і який захоплюється {hobby}."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()


def birthday(update: Update, context: CallbackContext):
    if len(context.args) >= 3:
        name = context.args[0]
        age = context.args[1]
        hobby = ' '.join(context.args[2:])
        greeting = generate_birthday_greeting(name, age, hobby)
        update.message.reply_text(greeting)
    else:
        update.message.reply_text("Будь ласка, введіть ім'я, вік і хобі після команди /birthday. Наприклад: /birthday Іван 30 риболовля.")


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('birthday', birthday))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

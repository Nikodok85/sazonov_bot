import telebot
import os
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")  # переменная окружения, будет установлена в Render
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Бот работает. Напиши вопрос или нажми кнопку."
    )

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@app.route('/', methods=['GET'])
def index():
    return 'Бот работает.'

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f"https://sazonov-bot.onrender.com/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

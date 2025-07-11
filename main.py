import os
import telebot
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@gynekolog_Sazonov"  # Замени на свой канал, если другой

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    message_text = update.message.text
    if message_text:
        bot.send_message(CHANNEL_ID, f"❓ Анонимный вопрос: «{message_text}»")
    return 'OK', 200

@app.route('/')
def webhook():
    return 'Working bot', 200

if __name__ == '__main__':
    app.run()

import telebot
from flask import Flask, request

TOKEN = "8027662725:AAEAydbYQxsA2ZbxOacgUlCzTgymzb4VBkM"
CHANNEL_ID = "-1006940287840"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    bot.send_message(CHANNEL_ID, f"❓ Анонимный вопрос: «{message.text}»")

@app.route('/', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/', methods=['GET'])
def index():
    return "Bot is alive", 200

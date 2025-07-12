from flask import Flask, request
import telebot
import os

TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = -1006940287840

bot = telebot.TeleBot(TOKEN)

WEBHOOK_URL = "https://sazonov-bot.onrender.com"

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("❓ Задать вопрос"))
    bot.send_message(
        message.chat.id,
        "Привет! 👋\n\nТы можешь задать анонимно любой вопрос по гинекологии.\n\nНажми кнопку ниже 👇",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "❓ Задать вопрос")
def ask_question(message):
    bot.send_message(
        message.chat.id,
        "✍️ Напиши свой вопрос — я получу его анонимно и опубликую с ответом в канале."
    )

@bot.message_handler(content_types=['text'])
def forward_to_channel(message):
    if message.text != "/start":
        try:
            print(f"📤 Пытаемся отправить в канал: {message.text}")
            bot.send_message(CHANNEL_ID, f"❓ Анонимный вопрос:\n\n{message.text}")
            bot.send_message(message.chat.id, "✅ Вопрос получен! Ждите ответ в канале.")
        except Exception as e:
            print(f"⚠️ Ошибка при отправке в канал: {e}")

@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        print(f"📩 Получен апдейт: {update}")  # Для отладки
        bot.process_new_updates([update])
        return "!", 200
    return "Not a Telegram request", 403

@app.route('/', methods=['GET'])
def index():
    return 'Бот работает!', 200

if __name__ == '__main__':
    print("Бот запущен!")  # <-- ДОБАВЬ ЭТУ СТРОКУ
    app.run(host="0.0.0.0", port=5000)

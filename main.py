from flask import Flask, request
import telebot
import os

# Получаем токен из переменной окружения
TOKEN = os.environ.get("TOKEN")

# ID твоего канала (положительное число для бота, даже если начинается с -100)
CHANNEL_ID = -1002113091552

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("❓ Задать вопрос"))
    bot.send_message(
        message.chat.id,
        "Привет! 👋\n\nТы можешь задать анонимно любой вопрос по гинекологии.\n\nНажми кнопку ниже 👇",
        reply_markup=markup
    )

# Обработка кнопки
@bot.message_handler(func=lambda message: message.text == "❓ Задать вопрос")
def ask_question(message):
    bot.send_message(
        message.chat.id,
        "✍️ Напиши свой вопрос — я получу его анонимно и опубликую с ответом в канале."
    )

# Обработка всех остальных текстов
@bot.message_handler(content_types=['text'])
def forward_to_channel(message):
    if message.text != "/start":
        try:
            text = message.text.strip()
            bot.send_message(CHANNEL_ID, f"❓ Анонимный вопрос:\n\n«{text}»")
            bot.send_message(message.chat.id, "✅ Вопрос получен! Ждите ответ в канале.")
        except Exception as e:
            print(f"⚠️ Ошибка при отправке в канал: {e}")
            bot.send_message(message.chat.id, "❌ Произошла ошибка при отправке. Попробуйте позже.")

# Вебхук
@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return 'ok', 200
    return 'not a telegram request', 403

# Проверка в браузере
@app.route('/', methods=['GET'])
def index():
    return 'Бот работает! ✅', 200

# Запуск локального сервера (на случай разработки)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

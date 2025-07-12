from flask import Flask, request
import telebot

app = Flask(__name__)

# Токен и ID канала
TOKEN = "8027662725:AAHd6lKQZhaqQp_MqYGhmztUVAcQF24XC3E"
CHANNEL_ID = "-1006940287840"  # обязательно с минусом

bot = telebot.TeleBot(TOKEN)

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("✍️ Задать вопрос"))
    bot.send_message(
        message.chat.id,
        "Привет! 👋\n\nТы можешь анонимно задать любой вопрос по гинекологии.\n\nНажми кнопку ниже ✍️",
        reply_markup=markup
    )

# Обработка кнопки
@bot.message_handler(func=lambda message: message.text == "✍️ Задать вопрос")
def ask_question(message):
    bot.send_message(
        message.chat.id,
        "✍🏻 Напиши свой вопрос — я получу его анонимно и опубликую с ответом в канале."
    )

# Обработка любого текста
@bot.message_handler(func=lambda message: True, content_types=['text'])
def forward_to_channel(message):
    if message.text != "✍️ Задать вопрос":
        bot.send_message(CHANNEL_ID, f"❓ Анонимный вопрос:\n{message.text}")
        bot.send_message(message.chat.id, "✅ Вопрос получен! Ждите ответ в канале.")

# Webhook endpoint
@app.route("/", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# Проверка доступности (необязательно, но полезно)
@app.route("/", methods=["GET"])
def index():
    return "Бот работает", 200

# Запуск локально (на Render не используется)
if __name__ == "__main__":
    app.run(debug=True)

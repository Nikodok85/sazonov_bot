from flask import Flask, request
import telebot

TOKEN = "8027662725:AAEAydbYQxsA2ZbxOacgUlCzTgymzb4VBkM"
CHANNEL_ID = -1006940287840  # ID твоего канала

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

# Обработка текстов
@bot.message_handler(content_types=['text'])
def forward_to_channel(message):
    if message.text != "/start":
        bot.send_message(CHANNEL_ID, f"❓ Анонимный вопрос:\n\n{message.text}")
        bot.send_message(message.chat.id, "✅ Вопрос получен! Ждите ответ в канале.")

# Webhook
@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return "!", 200
    return "Not a Telegram request", 403

# Health-check
@app.route('/', methods=['GET'])
def index():
    return 'Бот работает!', 200

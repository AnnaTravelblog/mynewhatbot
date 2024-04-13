from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.ext import CallbackContext
import os
import random
import requests
import time


TOKEN = '6791148515:AAGKmXAd3v3SpRsCRXyCG0emJk5F1SkF57s'
OPENWEATHERMAP_API_KEY = 'f98028a3cd35a770ee7e30d447f45301'
TRIPADVISOR_API_KEY = 'your_tripadvisor_api_key'
BASE_URL = f'https://api.telegram.org/bot{TOKEN}/'
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather?'

# Приветственные сообщения
GREETINGS = [
    "Привет! Я твой путешественник-бот. Готов помочь с планированием твоих следующих приключений!",
    "Здравствуй! Я готов отправиться с тобой в путешествие!",
    "Приветствую тебя, путешественник! Куда собираешься отправиться?",
    "Привет! Я здесь, чтобы помочь тебе с выбором следующего направления для путешествия."
]

DESTINATIONS = {
    "париж": "Париж - прекрасный город! Обязательно посети Эйфелеву башню и Лувр. Куда еще?"

             ,
    "токио": "Токио - удивительный город! Не пропусти Цукадзи и Сенсодзи. Куда еще?",
    "рим": "Рим - великолепный город! Посети Колизей и Ватикан.",

    "лондон": "Лондон - столица Великобритании! Посети Биг Бен и Британский музей.",

    "барселона": "Барселона - город архитектурных шедевров! Посети собор Святого Семейства и Парк Гуэль.",

    "нью-йорк":
        "Нью-Йорк - город, который никогда не спит! Открой для себя Манхэттен и Центральный парк.",

    "москва":
        "Москва - столица России! Посети Красную площадь и Кремль.",

    "киев":
         "Киев - древний город с богатой историей! Посети Софиевский собор и Подол.",

    "бангкок":
         "Бангкок - экзотический город в сердце Таиланда! Наслаждайся вкусной тайской кухней и посети храм Ват Арун.",

    "прага":
        "Прага - город старинных улочек и замков! Посети Карлов мост и Пражский град.",

    "дубай":
         "Дубай - город впечатляющих небоскребов и роскоши! Посети Бурдж Халифа и Дубай Молл.",

    "сидней":
         "Сидней - живописный город на побережье! Посети оперный театр и Сиднейский харбор.",

    "амстердам":
        "Амстердам - город каналов и великолепной архитектуры! Посети музей Ван Гога и Дом Анны Франк.",

    "флоренция":
        "Флоренция - исторический город с богатым культурным наследием! Посети Галерею Уффици и собор Санта-Мария-дель-Фьоре.",

    "киото":
         "Киото - древняя столица Японии с множеством храмов и садов! Посети Золотой павильон и храм Фушими Инари.",

    "сан-франциско":
         "Сан-Франциско - культурный и технологический центр США! Посети знаменитый мост Голден Гейт и остров Алькатрас.",

    "шанхай":
         "Шанхай - современный мегаполис с высокими небоскребами! Посети набережную Бунд и Ципао.",

    "кипр":
         "Кипр - остров любви и истории! Посети археологический парк Пафоса и монастырь Киккос.",

    "рио-де-жанейро":
         "Рио-де-Жанейро - город пляжей и карнавалов! Посети Христа-Искупителя и пляж Ипанема.",

    "сеул":
        "Сеул - космополитичный город с высокими технологиями! Посети дворец Гёнбоккун и Торговый центр Дунгдаемун.",

    "будапешт":
        "Будапешт - город с тысячелетней историей и термальными источниками! Посети Рыбацкий бастион и парламент.",

    "каир":
        "Каир - древний город с пирамидами и сфинксами! Посети пирамиду Хеопса и музей египетской античности.",

    "санкт-петербург":
        "Санкт-Петербург - северная столица России с богатым культурным наследием! Посети Эрмитаж и Петергоф.",

    "мельбурн":
         "Мельбурн - культурный и спортивный центр Австралии! Посети здание парламента и Royal Botanic Gardens.",

     "дублин":
         "Дублин - живописный город с историческими замками и пабами! Посети Замок Дублин и бар Темпл Бар.",

    "вена":
        "Вена - столица Австрии с красивой архитектурой и классической музыкой! Посети дворец Шенбрунн и кафе Централь.",

    "кишинев":
      "Кишинёв - столица Молдовы! Посети Национальный музей и Старую крепость.",

    "тирасполь":
        "Тирасполь - столица Приднестровской Молдавской Республики! Посети Приднестровский государственный университет и Парк Славы.",

    "пекин":
        "Пекин - столица Китая с богатой историей! Посети Запретный город и Великую Китайскую стену.",

    "мумбай":
         "Мумбай - крупнейший город Индии! Посети Ворота Индии и Храм Махалакшми.",

    "рейкьявик":
         "Рейкьявик - столица Исландии! Посети Холлгримскерку и смотровую площадку Перлан.",

    "санторини":
     "Санторини - жемчужина Эгейского моря! Посети город Фира и пляж Камари.",

    "венеция":
         "Венеция - город на воде! Посети площадь Сан-Марко и остров Мурано."}


def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text.lower()
    if "привет" in text or "здравствуй" in text:
        send_message(update.message.chat_id, "И тебе привет, добрый человек! В какой город едем?")
    elif text in DESTINATIONS:
        weather_info = get_weather_info(text)
        send_message(update.message.chat_id, f"{DESTINATIONS[text]}\n\n{weather_info}")
    elif "спасибо" in text:
        send_message(update.message.chat_id, "Пожалуйста, мой любимый путешественник! Куда еще?")
        time.sleep(4)
        send_message(update.message.chat_id, "Может, еще посмотрим какой-то другой город?")
    elif "с удовольствием" in text:
        send_message(update.message.chat_id, "Рад помочь!")
        # После 2 секунд спросим, может еще посмотрим другой город
        # Добавим обработку, чтобы бот говорил "Обращайся ко мне чаще, мой любимый путешественник!"
    elif "сейчас подумаю" in text or "сейчас" in text:
        send_message(update.message.chat_id, " Я жду, Обращайся ко мне чаще, мой любимый путешественник!")
        # После 4 секунд спросим, может еще посмотрим другой город
        time.sleep(4)
        send_message(update.message.chat_id, "Может, еще посмотрим какой-то другой город?")
    elif "посоветуй" in text or "а куда лучше?" in text:
        send_message(update.message.chat_id, " Я думаю Рим или София тебе точно подойдет. Сингапур, кстати тоже не плохой вариаент")
    else:
        send_message(update.message.chat_id, "Я не знаю такого места. Может быть, выберем что-то другое? Куда поедем?")

def get_weather_info(city: str) -> str:
    params = {'q': city, 'appid': OPENWEATHERMAP_API_KEY, 'units': 'metric', 'lang': 'ru'}
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"Погода в {city.capitalize()}: {weather_description}, Температура: {temperature}°C"
    else:
        return "Информация о погоде недоступна."

def send_message(chat_id, text, reply_markup=None):
    data = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': reply_markup
    }
    response = requests.post(BASE_URL + 'sendMessage', data=data)
    print(response.json())

def start(update, context):
    update.message.reply_text(random.choice(GREETINGS) + " В какой город вы хотите поехать?")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Обработчик команды /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Добавление обработчика для обычных текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
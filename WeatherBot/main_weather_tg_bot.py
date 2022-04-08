import requests
from bs4 import BeautifulSoup as bs
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Погода" , "Меню Пушкарев"]
    keyboard.add(*buttons)
    await message.reply(f"Привет, {message.from_user.username}! Выбери, что ты хочешь?!", reply_markup=keyboard)



@dp.message_handler(Text(equals="Погода"))
async def get_city_for_weather(message: types.Message):
    await message.reply(f"Введите название города в котором хотите узнать погоду")



@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = response.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри за окно,не пойму что там за погода!"
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        feels_like = data["main"]["feels_like"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\n"
                            f"Ощущается, как: {feels_like}C\nВетер: {wind} м/c\n"
                            f"Восход солнца: {sunrise_timestamp}\nЗаход солнца: {sunset_timestamp}\n"
                            f"Продолжительность светового дня: {length_of_the_day}\n"
                            f"Хорошего дня")
    except Exception as ex:
        await message.reply("\U00002620Проверьте название города\U00002620")

@dp.message_handler(Text(equals="Меню Пушкарев"))
async def get_menu(message):
    try:
        URl = "https://pushkarev.cafe/biznes-lanch"
        menu = "***МЕНЮ***\nСАЛАТЫ:\n"
        response = requests.get(URl)
        soup = bs(response.text, "lxml")
        dishes = soup.find_all('div', class_='item-list')
        menu += dishes[0].text + "\nСУПЫ:\n" + \
                dishes[1].text + "\nВТОРЫЕ БЛЮДА:\n" + \
                dishes[2].text + "\nГАРНИРЫ:\n" + \
                dishes[3].text + "\n\nНАПИТКИ:\n" + \
                dishes[4].text + "\n" + \
                dishes[5].text + "\n" + \
                dishes[6].text + "\n" + \
                dishes[7].text + "\n" + \
                dishes[8].text + "\n" + \
                dishes[9].text + "\n\nДЕСЕРТЫ:\n" + \
                dishes[10].text + "\n"

        await message.reply(menu)
    except Exception as ex:
        await message.reply("Ой, ошибочка вышла")


if __name__ == '__main__':
    executor.start_polling(dp)

import asyncio
import logging
import aiogram
from aiogram import Bot, Dispatcher, executor, types
import os
from os.path import join, dirname
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, chat
from aiogram.utils.json import json
from dotenv import load_dotenv
import speech_recognition as sr
from aiogram.dispatcher.filters import Command
def get_from_env(key):
    dotenv_path = join(dirname(__file__), 'token.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)


API_TOKEN = get_from_env('bot_token')
r = sr.Recognizer()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)



button_help = KeyboardButton('/help')
Keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_help)
inline_btn_1 = InlineKeyboardButton('Вывести небольшой пост о главном увлечении', callback_data='article')
inline_btn_2 = InlineKeyboardButton('Ссылка на публичный репозиторий с исходниками бота', url="https://github.com/")

inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1).add(inline_btn_2)
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer_sticker(r'CAACAgIAAxkBAALWc2TmqPkZYFREURw4_BfCmpiNg33GAALCIAACf1yASsTDAuAdKs3lMAQ')
    await asyncio.sleep(1)
    await message.answer(f'Рад тебя видеть, <b>{message.from_user.first_name}</b>.')
    await message.answer('Я - тестовое задание Киприяновой Маргариты.',reply_markup=Keyboard)
    await asyncio.sleep(1)
    await message.answer('Я знаю такие команды как: \n<b>/photoalbum</b> - <i>вывести последнее селфи и фото из старшей школы</i> \n<b>/voice</b> - <i>прислать войс на выбранную тему</i> ', reply_markup=inline_kb1)

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.answer('Я - тестовое задание Киприяновой Маргариты.')
    await asyncio.sleep(1)
    await message.answer(
        'Я знаю такие команды как: \n<b>/photoalbum</b> - <i>вывести последнее селфи и фото из старшей школы</i> \n<b>/voice</b> - <i>прислать войс на выбранную тему</i> ',
        reply_markup=inline_kb1)


@dp.message_handler(commands=['photoalbum'])
async def photoalbum(message: types.Message):
    await message.answer("Сейчас я покажу тебе несколько своих фото!")

    await types.ChatActions.upload_photo()

    media = types.MediaGroup()

    media.attach_photo('https://storage.yandexcloud.net/testtaskkidsaibot/20230822_155341.jpg', 'Это мое последнее селфи!')

    media.attach_photo('https://storage.yandexcloud.net/testtaskkidsaibot/KN-ijn58wu4.jpg', 'Как же давно я окончила школу...')

    await message.reply_media_group(media=media)

@dp.message_handler(commands=['voice'])
async def getVoice(message: types.Message):
    await message.answer("Давай я расскажу тебе историю! Какую ты хочешь?")
    await asyncio.sleep(1)
    await message.answer("Введи команду <b>/tell</b> и добавь после нее тему, которая тебе интересна (через пробел, например  /tell hello). \nВот про что я могу рассказать:\n<b>GPT</b> - <i>рассказ в формате «объясняю своей бабушке», что такое GPT</i>\n<b>SQL</b> - <i>максимально коротко объясняю разницу между SQL и NoSQL</i>\n<b>love</b> - <i>история первой любви</i>")
@dp.message_handler(commands=["tell"])
async def name(message: types.Message, command):
    if not command.args:
        await message.answer("Введи название истории после команды <b>/tell</b>!")
    elif command.args.lower()=="gpt":
        await bot.send_audio(message.chat.id, 'https://storage.yandexcloud.net/testtaskkidsaibot/audio1.ogg')
    elif command.args.lower()=="sql":
        await bot.send_audio(message.chat.id, 'https://storage.yandexcloud.net/testtaskkidsaibot/audio2.ogg')
    elif command.args.lower()=="love":
        await bot.send_audio(message.chat.id, 'https://storage.yandexcloud.net/testtaskkidsaibot/audio3.ogg')
    elif command.args.lower()=="hello":
        await bot.send_audio(message.chat.id, 'https://storage.yandexcloud.net/testtaskkidsaibot/audio4.ogg')
    else:
        await message.answer("Я не понимаю, какую историю ты хочешь попросить, попробуй еще раз😭")

@dp.callback_query_handler(lambda c: c.data == 'article')
async def process_callback_article(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Сложно сказать, какое увлечение я могу назвать <i>главным</i>.\nЭто зависит от того, что понимать под словом главный.\nДелом своей жизни я сделала программирование. В быту мне регулярно пригождаются навыки дизайна и готовки. А в свободное время я обожаю играть в компьютерные игры.')
    await asyncio.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'У меня есть аккаунт в Steam, на котором куплено уже 126 игр. Мне очень нравится получать достижения и проходить все на 100%, а потом делиться этим в своем профиле.')
    await asyncio.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'К сожалению, не все игры сейчас можно купить. Некоторые вышли так давно, что они сами, и консоли, для которых их разрабатывали, больше не продаются. На помощь приходят эмуляторы. Это виртуальные машины, имитирующие работу старых консолей. Иногда их бывает сложно настроить, но, когда получается – запуск игры приносит еще больше удовлетворения.')
    await asyncio.sleep(1)
    await bot.send_message(callback_query.from_user.id, 'Из жанров я предпочитаю adventure, action rpg и платформеры. Мне нравятся нишевые проекты с глубоким сюжетом. Последняя игра, которую я прошла, была Nier:Replicant. Сейчас я играю в Drakengard.')

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Прости, я не очень умный бот.")
    await asyncio.sleep(1)
    await message.answer("Я даже не знаю, что ответить тебе на "+message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
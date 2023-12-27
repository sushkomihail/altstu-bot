import logging
import math

import settings
import message_manager
from settings import Commands, Directories

from aiogram import Bot, Dispatcher, executor, types


logging.basicConfig(level=logging.INFO)
bot = Bot(settings.TOKEN, parse_mode=types.ParseMode.HTML)  # , proxy='http://proxy.server:3128'
dp = Dispatcher(bot)


@dp.message_handler(commands=Commands.START)
async def start_handler(message: types.Message) -> None:
    await message.answer('Введи:\n'
                         '<b><i>Номер задания(например, 1)</i></b>\n\n'
                         'или\n\n'
                         '<b><i>Номер задания + текст(желательно вводить только несколько слов)'
                         '(например, 1:текст)</i></b>\n\n'
                         '<b><i>Чтобы постотреть задания прошлых лет, поставь ! в начале запроса'
                         '(например, !1:текст)</i></b>')


@dp.message_handler(commands=Commands.HELP)
async def help_handler(message: types.Message) -> None:
    await message.answer(f'/{Commands.START} - начало работы с ботом\n'
                         f'/{Commands.HELP} - список команд\n')


@dp.message_handler()
async def economy_handler(message: types.Message) -> None:
    directory = Directories.ECONOMY
    message_text = message.text.strip().lower()

    if message_text[0] == '!':
        directory += 'old/'
        message_text = message_text[1:]

    if message_manager.is_number_correct(message_text, 1, 25):
        directory += str(int(message_text))
        photos = message_manager.get_photos(directory)
    else:
        input_words = message_text.split(':')

        if len(input_words) != 2 or input_words[1] == '' or not message_manager.is_number_correct(input_words[0], 1, 25):
            await message.answer('Вы ввели какую-то херню!')
            return

        directory += str(int(input_words[0]))
        photos = message_manager.get_photos_by_text(directory, input_words[1])
    await send_photos_group(message, directory, photos)


async def send_photos_group(message: types.Message, directory: str, photos: list) -> None:
    photos_count = len(photos)

    if photos_count == 0:
        await message.answer('Упс... А фотографий то нету!')
        return

    messages_count = math.ceil(photos_count / 10)
    remaining_photos_count = photos_count

    for i in range(messages_count):
        media_group = types.MediaGroup()
        photos_in_group_count = 10

        if remaining_photos_count < 10:
            photos_in_group_count = remaining_photos_count

        for j in range(photos_in_group_count):
            media_group.attach_photo(photo=types.InputFile(
                path_or_bytesio=f'{directory}/{photos[i * 10 + j]}'
            ))

        await message.answer_media_group(media=media_group)
        remaining_photos_count -= photos_in_group_count


def main() -> None:
    executor.start_polling(dp)

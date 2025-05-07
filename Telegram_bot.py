import Way
import Config
import asyncio
import logging
import data_handler
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

bot = Bot(token=Config.BotToken)
dp = Dispatcher()
Version = '10.0'


@dp.message(CommandStart())
async def cmd_start(message: Message):
    if data_handler.add_user(telegram_id=str(message.from_user.id), name=message.from_user.username) == 1:
        await message.answer(Config.hello_text[0])
        print(f'+ {message.from_user.id} {message.from_user.username}')
    else:
        await message.answer(Config.hello_text[1])


@dp.message(Command('help'))
async def get_help(message: Message):
    await message.answer(Config.help_message)


@dp.message(Command('way'))
async def way(message: Message):
    await message.answer(text="Выбери настроение(в зависимости от цвета волны): ",
                         reply_markup=await Way.color_of_path_keyboard())


@dp.message(Command('colors'))
async def colors_info(message: Message):
    await message.answer(text='Выберите цвет для просмотра описания:', reply_markup=await Way.colors_info_keyboard())


# описание цвета (вода про него)
@dp.callback_query(F.data.startswith("info_color_"))
async def call_back(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text=f"{callback.data[11:]}: {Config.colors[callback.data[11:]]}")


# выбор маршрута определенного цвета
@dp.callback_query(F.data.startswith("color_"))
async def call_back(callback: CallbackQuery):
    await callback.answer(text=f"Вы выбрали настроение {callback.data[6:]}")
    await callback.message.edit_text(text=callback.data[6:] + "\n Выберите один из доступных маршрутов:")
    await callback.message.edit_reply_markup(reply_markup=await Way.one_color_path(callback.data[6:]))


# вернуться к выбору маршрута
@dp.callback_query(F.data.startswith("back_to_color_"))
async def call_back(callback: CallbackQuery):
    await callback.message.edit_text(text="Выбери настроение(в зависимости от цвета волны): ",
                                     reply_markup=await Way.color_of_path_keyboard())


@dp.callback_query(F.data.startswith("path_"))
async def call_back(callback: CallbackQuery):
    try:
        await callback.message.answer_photo(photo=data_handler.get_link_of_path(callback.data[5:]))
    finally:
        await callback.message.answer(text=data_handler.get_text_of_path(way_name=callback.data[5:]),
                                      reply_markup=await Way.map_link_keyboard(way_name=callback.data[5:]))
        await callback.answer()


# @dp.message(F.text)
# async def get_text(message: Message):
#     print(message.from_user.username, message.text)
#     with open('blac_box.txt', 'a') as f:
#         f.write(f"{message.from_user.username}: {message.text} \n")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':

    if Config.TestMode:
        data_handler.create_database()
        Way.from_csv_to_db()
        logging.basicConfig(level=logging.INFO)

    try:
        print(f"Version: {Version}")
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

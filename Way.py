from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
import csv
import Config
import data_handler

ways = data_handler.get_list_of_ways()


async def colors_info_keyboard():
    keyboard = InlineKeyboardBuilder()
    for i in Config.colors.keys():
        keyboard.add(InlineKeyboardButton(text=i, callback_data=f"info_color_{i}"))
    return keyboard.as_markup()


async def color_of_path_keyboard():
    keyboard = InlineKeyboardBuilder()
    for i in Config.colors.keys():
        keyboard.add(InlineKeyboardButton(text=i, callback_data=f"color_{i}"))
    return keyboard.as_markup()


async def map_link_keyboard(way_name):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Открыть в навигаторе', url=data_handler.get_map_link_of_path(way_name=way_name)))
    return keyboard.as_markup()


async def one_color_path(color):
    keyboard = InlineKeyboardBuilder()
    for item in data_handler.get_one_color_paths(color):
        keyboard.add(InlineKeyboardButton(text=item[1], callback_data=f"path_{item[1]}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=f"back_to_color_{item[1]}"))
    return keyboard.as_markup()


# def get_media(way_name):
#     folder_path = rf"Ways\{way_name}"
#     media = []
#     for file_name in os.listdir(folder_path):
#         if os.path.isfile(os.path.join(folder_path, file_name)):
#             print(folder_path + '\\' + file_name)
#             media.append(
#                 InputMediaPhoto(path=folder_path + '\\' + file_name, input_type='photo')
#             )
#     return media


def from_csv_to_db(csv_file_path=fr"D:\PycharmProjects\ORG\ОРГ - Лист1(1).csv"):
    with open(csv_file_path, encoding="utf8", mode='r') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                data_handler.add_way(*row)
            except:
                pass

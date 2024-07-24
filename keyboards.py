from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import json


#------------------Создание клавиатуры для выбора фильма/сериала----------------------
def choise_keyboard() -> InlineKeyboardMarkup:
    commands = ['Фильмы', 'Сериалы']
    buttons = []
    for command in commands:
        if command == 'Фильмы':
            buttons.append(InlineKeyboardButton(text=command, callback_data='films'))
        if command == 'Сериалы':
            buttons.append(InlineKeyboardButton(text=command, callback_data='serials'))
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return inline_keyboard


#------------------Создание клавиатуры для подбора фильма----------------------
def films_keyboard(is_answer: bool) -> InlineKeyboardMarkup:
    with open('genres_of_films.json', 'r', encoding='utf-8') as f:
        genre_of_films = json.load(f)
    inline_buttons = [[] for _ in range(int(len(genre_of_films) / 4) + 1)]
    index = 0
    for name, id_films in genre_of_films.items():
        if len(inline_buttons[index]) == 4:
            index += 1
            inline_buttons[index].append(InlineKeyboardButton(text=name.capitalize(), callback_data=f'f{id_films}'))
        else:
            inline_buttons[index].append(InlineKeyboardButton(text=name.capitalize(), callback_data=f'f{id_films}'))
    viewed_or_favorite = []
    back = []
    if is_answer:
        viewed_or_favorite.append(InlineKeyboardButton(text='В избранное ⭐️', callback_data='lffavorite'))
        viewed_or_favorite.append(InlineKeyboardButton(text='Смотрел 👁‍', callback_data='mfwatched'))
        viewed_or_favorite.append(InlineKeyboardButton(text='Неинтересно', callback_data='nonfinteresting'))
    back.append(InlineKeyboardButton(text='🔙 Главное меню', callback_data='menu'))
    buttons = [*inline_buttons, viewed_or_favorite, back]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_keyboard


#------------------Создание клавиатуры для выбора сериала----------------------
def serials_keyboard(is_answer: bool) -> InlineKeyboardMarkup:
    with open('genres_of_serials.json', 'r', encoding='utf-8') as f:
        genre_of_serials = json.load(f)
    inline_buttons = [[] for _ in range(len(genre_of_serials)//4)]
    index = 0
    for name, id_serials in genre_of_serials.items():
        if len(inline_buttons[index]) == 4:
            index += 1
            inline_buttons[index].append(InlineKeyboardButton(text=name.capitalize(), callback_data=f's{id_serials}'))
        else:
            inline_buttons[index].append(InlineKeyboardButton(text=name.capitalize(), callback_data=f's{id_serials}'))
    viewed_or_favorite = []
    back = []
    if is_answer:
        viewed_or_favorite.append(InlineKeyboardButton(text='В избранное ⭐️', callback_data='lsfavorite'))
        viewed_or_favorite.append(InlineKeyboardButton(text='Смотрел 👁‍', callback_data='mswatched'))
        viewed_or_favorite.append(InlineKeyboardButton(text='Неинтересно', callback_data='nonsinteresting'))
    back.append(InlineKeyboardButton(text='🔙 Главное меню', callback_data='menu'))
    buttons = [*inline_buttons, viewed_or_favorite, back]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_keyboard


#------------------Создание клавиатуры для главной страницы----------------------
def main_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="Выбор фильма/сериала 📺"),
            KeyboardButton(text="Профиль👤")
        ],
        [
            KeyboardButton(text="Просмотренные фильмы/сериалы 📺"),
            KeyboardButton(text="Избранное ⭐️")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard


#------------------Создание клавиатуры для просмотреных фильмов/сериалов----------------------
def viewed_keyboard() -> InlineKeyboardMarkup:
    commands = ['Фильмы', 'Сериалы']
    buttons = []
    for command in commands:
        if command == 'Фильмы':
            buttons.append(InlineKeyboardButton(text=command, callback_data='vfilms'))
        if command == 'Сериалы':
            buttons.append(InlineKeyboardButton(text=command, callback_data='vserials'))
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return inline_keyboard


#------------------Создание клавиатуры для избранных фильмов/сериалов----------------------
def get_favorite_media() -> InlineKeyboardMarkup:
    commands = ['Фильмы', 'Сериалы']
    buttons = []
    for command in commands:
        if command == 'Фильмы':
            buttons.append(InlineKeyboardButton(text=command, callback_data='jffilms'))
        if command == 'Сериалы':
            buttons.append(InlineKeyboardButton(text=command, callback_data='jfserials'))
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return inline_keyboard

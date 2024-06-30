from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import json


def choise_keyboard():
    commands = ['Фильмы', 'Сериалы']
    buttons = []
    for command in commands:
        if command == 'Фильмы':
            buttons.append(InlineKeyboardButton(text=command, callback_data='films'))
        if command == 'Сериалы':
            buttons.append(InlineKeyboardButton(text=command, callback_data='serials'))
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return inline_keyboard

def films_keyboard():
    with open('genres_of_films.json', 'r', encoding='utf-8') as f:
        genre_of_films = json.load(f)
    inline_buttons = [[] for _ in range(int(len(genre_of_films) / 4) + 1)]
    index = 0
    for name, id in genre_of_films.items():
        if len(inline_buttons[index]) == 4:
            index += 1
            inline_buttons[index].append(InlineKeyboardButton(text=name.capitalize(), callback_data=f'f{id}'))
        else:
            inline_buttons[index].append(InlineKeyboardButton(text=name.capitalize(), callback_data=f'f{id}'))
    back = [InlineKeyboardButton(text='🔙 Назад', callback_data='back'), InlineKeyboardButton(text='Посмотрел', callback_data='watched')]
    buttons = [*inline_buttons, back]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_keyboard


def serials_keyboard():
    with open('genres_of_serials.json', 'r', encoding='utf-8') as f:
        genre_of_serials = json.load(f)
    inline_buttons = [[] for i in range(len(genre_of_serials)//4)]
    index = 0
    for name, id in genre_of_serials.items():
        if len(inline_buttons[index]) == 4:
            index += 1
            inline_buttons[index].append(InlineKeyboardButton(text=name.capitalize(), callback_data=f's{id}'))
        else:
            inline_buttons[index].append(InlineKeyboardButton(text=name.capitalize(), callback_data=f's{id}'))
    back = [InlineKeyboardButton(text='🔙 Назад', callback_data='back')]
    buttons = [*inline_buttons, back]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_keyboard

def main_keyboard():
    kb = [
        [
            KeyboardButton(text="Выбор фильма/сериала 🎞️"),
            KeyboardButton(text="👤Профиль")
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard
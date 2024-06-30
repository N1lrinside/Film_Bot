from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards import main_keyboard, films_keyboard, serials_keyboard, choise_keyboard
from models import Films, Session, Serials, User, WatchedFilms
from sqlalchemy import func
from sqlalchemy.future import select
from datetime import datetime

router = Router()
data = {}


@router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer(f"🎬 Привет! Я бот, который поможет тебе подобрать фильмы и сериалы. ", reply_markup=main_keyboard())


@router.message(F.text == 'Выбор фильма/сериала 🎞️')
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Выбери, что будешь смотреть, и я найду для тебя что-нибудь интересное! 📺🍿", reply_markup=choise_keyboard())


@router.message(F.text == '👤Профиль')
async def get_profile_user(message: Message):
    await message.answer(f"Ваш профиль, {message.from_user.full_name} 👤"
                         f"Кол-во просмотренных фильмов: 0 🎬"
                         f"Ваши любимые жанры: Информация отсутствует 📄")


@router.callback_query(F.data == 'films')
async def callback_query_handler_films(query: CallbackQuery) -> None:
    await query.message.edit_text('Какой жанр? 🎥', reply_markup=films_keyboard())


@router.callback_query(F.data == 'serials')
async def callback_query_handler_serials(query: CallbackQuery) -> None:
    await query.message.edit_text('Какой жанр? 🎥', reply_markup=serials_keyboard())


@router.callback_query(lambda call: call.data[0] == 'f' or call.data[0] == 's')
async def random_films_or_serials(query: CallbackQuery) -> None:
    type_media = query.data[0]
    genre_id = query.data[1:]
    stmt = select(Films).where(Films.genre == genre_id).order_by(func.random()).limit(1) if type_media == 'f' \
        else select(Serials).where(Serials.genre == genre_id).order_by(func.random()).limit(1)
    result = await Session.execute(stmt)
    vse_films = result.scalar_one_or_none()

    message_text = (
            f"Название: {vse_films.name} 🎬\n"
            f"Описание: {vse_films.overview[:900]}\n"
            f"Рейтинг: {vse_films.rating}⭐️\n"
            f"Дата выхода: {datetime.strftime(vse_films.release_date, '%d-%m-%Y')} 📅"
        )

    if type_media == 'f':
        await query.message.answer_photo(vse_films.poster, caption=message_text, reply_markup=films_keyboard())
        data[query.from_user.id] = {
            'film_id': vse_films.id,
            'genre_id': vse_films.genre
        }
    else:
        await query.message.answer_photo(vse_films.poster, caption=message_text, reply_markup=serials_keyboard())
    Session.close()


@router.callback_query(F.data == 'back')
async def back(callback: CallbackQuery):
    await callback.message.answer(f'Выбери, что будешь смотреть, и я найду для тебя что-нибудь интересное! 📺🍿',
                                  reply_markup=choise_keyboard())

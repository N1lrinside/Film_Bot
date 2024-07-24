from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards import (main_keyboard, films_keyboard, serials_keyboard,
                       choise_keyboard, viewed_keyboard, get_favorite_media)
from models import Films, Session, Serials, User, WatchedFilms, WatchedSerials
from sqlalchemy import func
from sqlalchemy.future import select
from datetime import datetime

router = Router()


#------------------Начало работы бота с команды /start----------------------
@router.message(CommandStart())
async def command_start(message: Message) -> None:
    async with Session() as session:
        async with session.begin():
            # Проверяем, существует ли пользователь
            stmt = select(User).filter_by(id_user=str(message.from_user.id))
            result = await session.execute(stmt)
            user = result.scalars().first()

            # Если пользователь не существует, создаем его
            if not user:
                user = User(id_user=str(message.from_user.id))
                session.add(user)
                await session.commit()  # Сохраняем изменения

    await message.answer(f"🎬 Привет! Я бот, который поможет тебе подобрать фильмы и сериалы. ",
                         reply_markup=main_keyboard())


#------------------Выбор фильма/сериала----------------------
@router.message(F.text == 'Выбор фильма/сериала 📺')
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Выбери, что будешь смотреть, и я найду для тебя что-нибудь интересное! 📺🍿",
                         reply_markup=choise_keyboard())


#------------------Профиль пользователя со статистикой----------------------
@router.message(F.text == 'Профиль👤')
async def get_profile_user(message: Message):
    async with Session() as session:
        async with session.begin():
            stmt = select(WatchedFilms).where(
                (WatchedFilms.id_user == str(message.from_user.id)) & (WatchedFilms.watched == True))
            result = await session.execute(stmt)
            films = result.scalars().all()
            stmt = select(WatchedSerials).where(
                (WatchedSerials.id_user == str(message.from_user.id)) & (WatchedSerials.watched == True))
            result = await session.execute(stmt)
            serials = result.scalars().all()
            stmt = select(WatchedFilms).where(
                (WatchedFilms.id_user == str(message.from_user.id)) & (WatchedFilms.favorite == True))
            result = await session.execute(stmt)
            favorite_films = result.scalars().all()
            stmt = select(WatchedSerials).where(
                (WatchedSerials.id_user == str(message.from_user.id)) & (WatchedSerials.favorite == True))
            result = await session.execute(stmt)
            favorite_serials = result.scalars().all()
    await message.answer(f"Ваш профиль, {message.from_user.full_name} 👤\n"
                         f"Кол-во просмотренных фильмов: {len(films)}🎬\n"
                         f"Кол-во просмотренных сериалов: {len(serials)//10}🎬\n"
                         f"Кол-во избранных фильмов: {len(favorite_films)}🎬\n"
                         f"Кол-во избранных сериалов: {len(favorite_serials)}🎬\n"
                         f"Ваши любимые жанры: Информация отсутствует 📄")


#------------------Просмотренные фильмы/сериалы----------------------
@router.message(F.text == 'Просмотренные фильмы/сериалы 📺')
async def check_viewed(message: Message):
    await message.answer('Выбери фильм/сериал📺🍿', reply_markup=viewed_keyboard())


#------------------Избранные фильмы/сериалы----------------------
@router.message(F.text == 'Избранное ⭐️')
async def check_favorite(message: Message):
    await message.answer('Выбери 📺🍿', reply_markup=get_favorite_media())


@router.callback_query(lambda call: call.data == 'vfilms' or call.data == 'vserials')
async def get_viewed(callback: CallbackQuery):
    id_user = str(callback.from_user.id)
    async with Session() as session:
        async with session.begin():
            if callback.data == 'vfilms':
                # Запрос для получения всех просмотренных фильмов пользователя
                stmt = select(Films.name).join(WatchedFilms, Films.id == WatchedFilms.id_film).where(
                    (WatchedFilms.id_user == id_user) & (WatchedFilms.watched == True)
                )
            else:
                # Запрос для получения всех просмотренных сериалов пользователя
                stmt = select(Serials.name).join(WatchedSerials, Serials.id == WatchedSerials.id_serial).where(
                    (WatchedSerials.id_user == id_user) & (WatchedSerials.watched == True)
                )
            result = await session.execute(stmt)
            viewed_items = result.scalars().all()
    if callback.data == 'vfilms':
        message_text = "Ваши просмотренные фильмы:\n" + "\n".join(viewed_items)
    else:
        message_text = "Ваши просмотренные сериалы:\n" + "\n".join(viewed_items)

    await callback.message.answer(message_text)


@router.callback_query(lambda call: call.data == 'films' or call.data == 'serials')
async def callback_query_handler_films(callback: CallbackQuery) -> None:
    if callback.data[0] == 'f':
        await callback.message.edit_text('Какой жанр? 🎥', reply_markup=films_keyboard(False))
    else:
        await callback.message.edit_text('Какой жанр? 🎥', reply_markup=serials_keyboard(False))


@router.callback_query(lambda call: call.data[0] == 'f' or call.data[0] == 's')
async def call_random_media_with_genre(callback: CallbackQuery, type_media: str = '', genre_id: str = ''):
    if not type_media:
        type_media = callback.data[0]
        genre_id = callback.data[1:]
    async with Session() as session:
        async with session.begin():
            subquery = select(WatchedFilms.id_film).where(
                (WatchedFilms.id_user == str(callback.from_user.id)) & ((WatchedFilms.watched == True) | (WatchedFilms.interesting == False))
            ) if type_media == 'f' else select(WatchedSerials.id_serial).where(
                (WatchedSerials.id_user == str(callback.from_user.id)) & ((WatchedSerials.watched == True) | (WatchedSerials.interesting == False))
            )

            stmt = select(Films).where(
                (Films.genre == genre_id) & (Films.id.notin_(subquery))
            ).order_by(func.random()).limit(1) if type_media == 'f' else select(Serials).where(
                (Serials.genre == genre_id) & (Serials.id.notin_(subquery))
            ).order_by(func.random()).limit(1)

            result = await session.execute(stmt)
            media = result.scalar_one_or_none()

            stmt = select(User).filter_by(id_user=str(callback.from_user.id))
            result = await session.execute(stmt)
            user = result.scalars().first()

            if type_media == 'f':
                user.film_id = media.id
                user.genre_id = genre_id
            else:
                user.serial_id = media.id
                user.genre_id = genre_id

            await session.commit()  # Сохраняем изменения
    if media:
        message_text = (
            f"Название: {media.name} 🎬\n"
            f"Описание: {media.overview[:900] if media.overview else 'Описание отсутствует'}\n"
            f"Рейтинг: {round(media.rating, 1)}⭐️\n"
            f"Дата выхода: {datetime.strftime(media.release_date, '%d-%m-%Y')} 📅"
        )
    else:
        message_text = ('Не получилось подобрать фильм/сериал.\nВозможно кол-во фильмов/сериалов по этому жанру закончились')
    if type_media == 'f':
        await callback.message.answer_photo(media.poster, caption=message_text, reply_markup=films_keyboard(True))
    else:
        await callback.message.answer_photo(media.poster, caption=message_text, reply_markup=serials_keyboard(True))


@router.callback_query(F.data[2:] == 'back')
async def back(callback: CallbackQuery):
    if callback.data[1] == 'f':
        await callback.message.answer('Какой жанр? 🎥', reply_markup=films_keyboard(False))
    else:
        await callback.message.answer('Какой жанр? 🎥', reply_markup=serials_keyboard(False))


@router.callback_query(lambda call: call.data == 'mfwatched' or call.data == 'mswatched' or
                                    call.data == 'lffavorite' or call.data == 'lsfavorite' or
                       call.data == 'nonfinteresting' or call.data == 'nonsinteresting')
async def watched_film(callback: CallbackQuery):
    id_user = str(callback.from_user.id)
    async with Session() as session:
        async with session.begin():
            # Получаем данные сессии пользователя из базы данных
            stmt = select(User).filter_by(id_user=id_user)
            result = await session.execute(stmt)
            user = result.scalars().first()
            genre_id = user.genre_id
            if callback.data[1:3] == 'fw':
                watched_film = WatchedFilms(id_film=user.film_id, id_user=id_user, watched=True)
                session.add(watched_film)
            if callback.data[1:3] == 'sw':
                watched_serial = WatchedSerials(id_serial=user.serial_id, id_user=id_user, watched=True)
                session.add(watched_serial)
            if callback.data[1:3] == 'ff':
                favorite_film = WatchedFilms(id_film=user.film_id, id_user=id_user, favorite=True)
                session.add(favorite_film)
            if callback.data[1:3] == 'sf':
                favorite_serial = WatchedSerials(id_serial=user.serial_id, id_user=id_user, favorite=True)
                session.add(favorite_serial)
            if callback.data[3:5] == 'fi':
                favorite_film = WatchedFilms(id_film=user.film_id, id_user=id_user, interesting=False)
                session.add(favorite_film)
            if callback.data[3:5] == 'si':
                favorite_serial = WatchedSerials(id_serial=user.serial_id, id_user=id_user, favorite=False)
                session.add(favorite_serial)
            user.film_id = None
            user.genre_id = None
            user.serial_id = None
        await session.commit()
    if callback.data[1] == 'f' or callback.data[3] == 'f':
        await call_random_media_with_genre(callback, 'f', genre_id)
    else:
        await call_random_media_with_genre(callback, 's', genre_id)


@router.callback_query(F.data == 'menu')
async def go_to_main_menu(callback: CallbackQuery):
    await callback.message.answer(f"Выбери, что будешь смотреть, и я найду для тебя что-нибудь интересное! 📺🍿",
                                  reply_markup=choise_keyboard())


@router.callback_query(lambda call: call.data == 'jffilms' or call.data == 'jfserials')
async def go_to_favorite_list(callback: CallbackQuery):
    id_user = str(callback.from_user.id)
    async with Session() as session:
        async with session.begin():
            if callback.data == 'jffilms':
                # Запрос для получения всех избранных фильмов пользователя
                stmt = select(Films.name, Films.genre_name).join(WatchedFilms, Films.id == WatchedFilms.id_film).where(
                    (WatchedFilms.id_user == id_user) & (WatchedFilms.favorite == True)
                )
            else:
                # Запрос для получения всех избранных сериалов пользователя
                stmt = select(Serials.name, Serials.genre_name).join(WatchedSerials,
                                                                     Serials.id == WatchedSerials.id_serial).where(
                    (WatchedSerials.id_user == id_user) & (WatchedSerials.favorite == True)
                )
            result = await session.execute(stmt)
            viewed_items = result.all()

    # Формирование текста сообщения
    if callback.data == 'jffilms':
        message_text = "Ваши избранные фильмы:\n"
        for name, genre_name in viewed_items:
            message_text += f"{name} (Жанр: {genre_name})\n"
    else:
        message_text = "Ваши избранные сериалы:\n"
        for name, genre_name in viewed_items:
            message_text += f"{name} (Жанр: {genre_name})\n"

    await callback.message.answer(message_text)

@router.message(F.text)
async def uncorrect_command(message: Message):
    if message.text not in ['Выбор фильма/сериала 🎞️', '👤Профиль', 'Просмотренные фильмы/сериалы', 'Избранное ⭐️']:
        await message.answer('Несуществующая команда 😢')
        await message.answer(f"Выбери, что будешь смотреть, и я найду для тебя что-нибудь интересное! 📺🍿",
                                      reply_markup=choise_keyboard())
import os
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, AsyncSession
from dotenv import load_dotenv

load_dotenv()

engine = create_async_engine(os.getenv('URL_DB'))
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


#------------------Создание образа модели----------------------
class Base(AsyncAttrs, DeclarativeBase):
    pass


#------------------Создание модели для Фильмов----------------------
class Films(Base):
    __tablename__ = 'Films'
    id = Column(Integer, primary_key=True)
    genre = Column(Integer)          # id жанра
    genre_name = Column(String)
    name = Column(String, unique=True)
    overview = Column(String, default='Описание отсутствует')
    rating = Column(Float, default='Рейтинг отсутствует')
    release_date = Column(Date)
    poster = Column(String)
    watched_films = relationship("WatchedFilms", back_populates="film")


#------------------Создание модели для Сериалов----------------------
class Serials(Base):
    __tablename__ = 'Serials'
    id = Column(Integer, primary_key=True)
    genre = Column(Integer)
    genre_name = Column(String)
    name = Column(String, unique=True)
    overview = Column(String, default='Описание отсутствует')
    rating = Column(Float, default='Рейтинг отсутствует')
    release_date = Column(Date)
    poster = Column(String)
    watched_serials = relationship("WatchedSerials", back_populates="serial")


#------------------Создание модели для Пользователя----------------------
class User(Base):
    __tablename__ = 'User'
    id_user = Column(String, primary_key=True, unique=True)
    film_id = Column(Integer, nullable=True, default=None)
    serial_id = Column(Integer, nullable=True, default=None)
    genre_id = Column(String, nullable=True, default=None)
    watched_films = relationship('WatchedFilms', back_populates='user')
    watched_serials = relationship("WatchedSerials", back_populates="user")


#------------------Создание модели для Статистики о фильмах----------------------
class WatchedFilms(Base):
    __tablename__ = 'WatchedFilms'
    id = Column(Integer, primary_key=True)
    id_user = Column(String, ForeignKey('User.id_user'))
    id_film = Column(Integer, ForeignKey('Films.id'))
    watched = Column(Boolean, default=False)
    favorite = Column(Boolean, default=False)
    interesting = Column(Boolean, default=True)
    user = relationship('User', back_populates='watched_films')
    film = relationship("Films", back_populates="watched_films")


#------------------Создание модели для Статистики о сериалах----------------------
class WatchedSerials(Base):
    __tablename__ = 'WatchedSerials'
    id = Column(Integer, primary_key=True)
    id_user = Column(String, ForeignKey('User.id_user'))
    id_serial = Column(Integer, ForeignKey('Serials.id'))
    watched = Column(Boolean, default=False)
    favorite = Column(Boolean, default=False)
    interesting = Column(Boolean, default=True)
    user = relationship('User', back_populates='watched_serials')
    serial = relationship("Serials", back_populates="watched_serials")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

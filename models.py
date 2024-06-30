import os
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, AsyncSession
from dotenv import load_dotenv

load_dotenv()

engine = create_async_engine(os.getenv('URL_DB'))
Session = AsyncSession(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Films(Base):
    __tablename__ = 'Films'
    id = Column(Integer, primary_key=True)
    genre = Column(String)
    name = Column(String, unique=True)
    overview = Column(String, default='Описание отсутствует')
    rating = Column(Float, default='Рейтинг отсутствует')
    release_date = Column(Date)
    poster = Column(String)
    watched_films = relationship("WatchedFilms", back_populates="film")

class Serials(Base):
    __tablename__ = 'Serials'
    id = Column(Integer, primary_key=True)
    genre = Column(String)
    name = Column(String, unique=True)
    overview = Column(String, default='Описание отсутствует')
    rating = Column(Float, default='Рейтинг отсутствует')
    release_date = Column(Date)
    poster = Column(String)


class User(Base):
    __tablename__ = 'User'
    id_user = Column(Integer, primary_key=True, unique=True)
    watched_films = relationship('WatchedFilms', back_populates='user')


class WatchedFilms(Base):
    __tablename__ = 'WatchedFilms'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('User.id_user'), default=0)
    id_film = Column(Integer, ForeignKey('Films.id'))
    watched = Column(Boolean, default=False)
    favorite = Column(Boolean, default=False)
    user = relationship('User', back_populates='watched_films')
    film = relationship("Films", back_populates="watched_films")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def shutdown():
    await engine.dispose()
    await Session.close()

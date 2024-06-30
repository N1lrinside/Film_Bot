import asyncio
import sys
import os
import logging
from aiogram import Bot, Dispatcher
from handlers import router
from dotenv import load_dotenv
from models import async_main, shutdown, Session


async def main() -> None:
    await async_main()
    load_dotenv()
    bot = Bot(token=os.getenv('TG_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        Session.close()
        print('Exit')

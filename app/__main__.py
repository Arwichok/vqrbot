import logging
import os
import sqlite3

import aiohttp
from aiogram import Dispatcher, Bot, executor

from app import handlers
from app.constants import SESSION, DB_FILE
from app.middlewares import VarsMiddleware
from app.models import init_models


async def on_startup(dp: Dispatcher):
    handlers.register(dp)
    dp[SESSION] = aiohttp.ClientSession()
    connection = sqlite3.connect(DB_FILE)
    init_models(connection)
    dp.middleware.setup(VarsMiddleware(dp[SESSION], connection))


async def on_shutdown(dp: Dispatcher):
    await dp[SESSION].close()


def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(os.environ.get("TOKEN"))
    dp = Dispatcher(bot)
    executor.start_polling(
        dispatcher=dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True
    )


if __name__ == '__main__':
    main()

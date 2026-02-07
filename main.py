import asyncio
import logging

from aiogram import Bot, Dispatcher
from app.config.cosy import token
from app.handlers.commands import router
from app.handlers.callback import router1

bot = Bot(token)
dp = Dispatcher()

async def main():
    dp.include_routers(router, router1) 
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit :)")
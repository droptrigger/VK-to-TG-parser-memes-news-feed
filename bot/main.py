import asyncio

from aiogram import Bot, Dispatcher
from checker import check
from handlers.user_handlers import router
from bot.data.config import TOKEN_TG


async def start_tg() -> None:
    """Entry point"""
    while True:
        bot = Bot(TOKEN_TG)
        dp = Dispatcher()
        dp.include_router(router)
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)
        except Exception as ex:
            print(f"entry error: {ex}")
            await asyncio.sleep(10)


print("tg bot started")
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(start_tg(), check()))
    except Exception as _ex:
        print(f"start error: {_ex}")

from config import bot, dp
import logging
import asyncio
from handlers.user.routers import user_router
from service.scheduler import scheduler


async def main():
    logging.basicConfig(level=logging.INFO)

    await bot.delete_webhook(drop_pending_updates=True)

    async def start_scheduler():
        logging.info("Starting scheduler...")
        while True:
            await scheduler()
            await asyncio.sleep(5)

    asyncio.create_task(start_scheduler())
    dp.include_router(user_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

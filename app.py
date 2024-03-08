from celery.schedules import crontab

from config import bot, dp
import logging
import asyncio
from handlers.user.routers import user_router
from service.celery_app import app


async def main():
    logging.basicConfig(level=logging.INFO)

    await bot.delete_webhook(drop_pending_updates=True)

    async def start_scheduler():
        print("Starting scheduler...")
        await asyncio.sleep(10)

        app.conf.beat_schedule = {
            'send-message-task': {
                'task': 'tasks.schedule_messages',
                'schedule': crontab(minute='*/5'),
            }
        }

    asyncio.create_task(start_scheduler())
    dp.include_router(user_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

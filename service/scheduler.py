import asyncio
import json
import logging

from sqlalchemy.future import select
from datetime import datetime, timedelta
from service.wb import search_article_from_wb
from config import session, bot, redis_client
from data.models import User


async def send_message(user_id, article_id):
    data = await search_article_from_wb(article_id)

    await bot.send_message(user_id, f"<b>Артикул товара: {article_id}</b>\n"
                                    f"\n"
                                    f"<b>Название:</b> {data['data']['products'][0]['name']}\n"
                                    f"<b>Артикул:</b> {data['data']['products'][0]['id']}\n"
                                    f"<b>Цена:</b> {data['data']['products'][0]['priceU']/ 100:.2f} RUB\n"
                                    f"<b>Цена со скидкой:</b> {data['data']['products'][0]['salePriceU']/ 100:.2f} RUB\n"
                                    f"<b>Рейтинг товара:</b> {data['data']['products'][0]['reviewRating']}\n"
                                    f"<b>Количество на всех складах:</b> {sum(stock['qty'] for stock in data['data']['products'][0]['sizes'][0]['stocks'])}",
                           parse_mode='HTML')

    logging.info(f"Send message to {user_id}")

    current_time = datetime.now().time()
    time_delta = timedelta(seconds=300)

    new_time = (datetime.combine(datetime.today(), current_time) + time_delta).time()

    redis_key = f"subscription:{article_id}"
    redis_value = redis_client.get(redis_key)

    redis_data = json.loads(redis_value)

    redis_data["next_message"] = new_time.strftime("%H:%M:%S")
    redis_value = json.dumps(redis_data)

    redis_client.set(redis_key, redis_value)


async def scheduler():
    users = session.scalars(select(User))

    for user in users:

        redis_key = f"subscription:{user.article_id}"
        redis_value = redis_client.get(redis_key)

        if redis_value:
            redis_data = json.loads(redis_value)
            last_message_time = datetime.strptime(redis_data["next_message"], "%H:%M:%S")

            if last_message_time.time() <= datetime.now().time():
                await send_message(redis_data['user_id'], user.article_id)
        else:
            pass

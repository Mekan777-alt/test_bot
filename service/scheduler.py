from sqlalchemy.future import select
from datetime import datetime
from service.wb import search_article_from_wb
from config import session, bot, redis_client
from data.models import User
from celery_app import app


@app.task
async def send_message(user_id, article_id, current_time):
    data = await search_article_from_wb(article_id)

    await bot.send_message(user_id, f"<b>Артикул товара: {article_id}</b>\n"
                                    f"\n"
                                    f"<b>Название:</b> {data['data']['products'][0]['name']}\n"
                                    f"<b>Артикул:</b> {data['data']['products'][0]['id']}\n"
                                    f"<b>Цена:</b> {data['data']['products'][0]['priceU']/ 100:.2f} RUB\n"
                                    f"<b>Цена со скидкой:</b> {data['data']['products'][0]['salePriceU']/ 100:.2f} RUB\n"
                                    f"<b>Рейтинг товара:</b> {data['data']['products'][0]['reviewRating']}\n"
                                    f"<b>Количество на всех складах:</b> {data['data']['products'][0]['sizes'][0]['stocks'][0]['qty']}",
                           parse_mode='HTML')

    redis_key = f"last_message_time:{user_id}"
    redis_client.set(redis_key, datetime.now().isoformat())


@app.task
def schedule_messages():
    users = session.scalars(select(User))

    for user in users:
        redis_key = f"last_message_time:{user.user_id}"
        last_message_time = redis_client.get(redis_key)

        if last_message_time is None or (datetime.now() - datetime.fromisoformat(last_message_time)).total_seconds() >= 300:
            send_message.apply_async(args=[user.user_id, user.article_id])

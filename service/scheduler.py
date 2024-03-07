import asyncio
from sqlalchemy.future import select
from datetime import datetime, timedelta
from service.wb import search_article_from_wb
from config import session, bot
from data.models import User


async def send_message(user_id, article_id, current_time):
    data = await search_article_from_wb(article_id)

    await bot.send_message(user_id, f"<b>Артикул товара: {article_id}</b>\n"
                                    f"\n"
                                    f"<b>Название:</b> {data['data']['products'][0]['name']}\n"
                                    f"<b>Артикул:</b> {data['data']['products'][0]['id']}\n"
                                    f"<b>Цена:</b> {data['data']['products'][0]['priceU']} RUB\n"
                                    f"<b>Рейтинг товара:</b> {data['data']['products'][0]['rating']}\n"
                                    f"<b>Количество на всех складах:</b> {data['data']['products'][0]['sizes'][0]['stocks'][0]['qty']}",
                           parse_mode='HTML')

    print("Сообщение отправилось")

    user = session.query(User).filter(User.user_id == user_id).first()

    current_datetime = datetime.combine(datetime.now(), current_time)

    time_delta = current_datetime + timedelta(minutes=5)

    user.next_message = time_delta
    session.commit()


async def scheduler():
    while True:
        current_time = datetime.now().time()

        users = session.scalars(select(User))

        for user in users:
            if user.next_message is not None and (current_time >= user.next_message):

                await send_message(user.user_id, user.article_id, current_time)

        await asyncio.sleep(10)

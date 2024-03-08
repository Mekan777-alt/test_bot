from config import session, redis_client
from sqlalchemy.future import select
from data.models import User


async def get_data_from_redis(user_id):
    users = session.scalars(select(User).where(User.user_id == str(user_id)))

    subscription_list = []

    for user in users:
        user_subscriptions = redis_client.keys(f"subscription:*{user.article_id}")

        if user_subscriptions:
            numbers_str = user_subscriptions[0][len("subscription:"):].decode('utf-8')
            subscription_list.append(numbers_str)
        else:
            pass

    return subscription_list if subscription_list else None


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


def main_markup():

    buttons = [
        [KeyboardButton(text='👉 Получить информацию по товару')],
        [KeyboardButton(text='👉 Остановить уведомления')],
        [KeyboardButton(text='👉 Получить информацию из БД')]
    ]

    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    return markup


class CallbackDataSubscribe(CallbackData, prefix='subscribe'):
    action: str


def subscribe(article_id):
    builder = InlineKeyboardBuilder()

    builder.button(text='👉 Подписаться', callback_data=CallbackDataSubscribe(action=str(article_id)))

    builder.adjust(1)

    return builder.as_markup()


class CallbackDataUnsubscribe(CallbackData, prefix='unsubscribe'):
    action: str
    data: str


async def create_unsubscribe_markup(subscriptions_list):
    builder = InlineKeyboardBuilder()

    for subscription in subscriptions_list:
        builder.button(text=subscription, callback_data=CallbackDataUnsubscribe(action=str(subscription),
                                                                                data=str(subscription)))
    builder.adjust(1)
    return builder.as_markup()




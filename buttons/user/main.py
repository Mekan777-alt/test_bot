from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from data.models import User
from sqlalchemy.future import select
from config import session


def main_markup():

    buttons = [
        [KeyboardButton(text='👉 Получить информацию по товару')],
        [KeyboardButton(text='👉 Остановить уведомления')],
        [KeyboardButton(text='👉 Получить информацию из БД')]
    ]

    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    return markup


def subscribe():

    button = [
        [InlineKeyboardButton(text='👉 Подписаться', callback_data='subscribe')]
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=button)

    return markup


class CallbackDataUnsubscribe(CallbackData, prefix='unsubscribe'):
    action: str
    data: str


def unsubscribe(user_id):

    builder = InlineKeyboardBuilder()

    users = session.scalars(select(User).where(User.user_id == str(user_id)))

    for user in users:

        if user.next_message:

            builder.button(
                text=user.article_id, callback_data=CallbackDataUnsubscribe(data=str(user.article_id),
                                                                            action=str(user.article_id)))
        else:
            pass
    builder.adjust(1)

    return builder.as_markup()




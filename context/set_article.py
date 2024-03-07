from aiogram.fsm.state import State, StatesGroup


class SetArticle(StatesGroup):
    article = State()


class UnSubscribe(StatesGroup):
    article = State()

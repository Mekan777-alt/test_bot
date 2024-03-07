from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from context.set_article import UnSubscribe
from config import session
from data.models import User
from buttons.user.main import main_markup, unsubscribe, CallbackDataUnsubscribe
from sqlalchemy.future import select

router = Router()


@router.message(F.text == '👉 Остановить уведомления')
async def stop_notification(message: types.Message, state: FSMContext):
    try:
        users = session.scalar(
            select(User).where(User.user_id == str(message.from_user.id), User.next_message != None))

        if users:
            await message.answer("Выберите артикул от которого хотите отписаться",
                                 reply_markup=unsubscribe(message.from_user.id))
            await state.set_state(UnSubscribe.article)
        else:

            await message.answer("Вы пока не подписались на обновления", reply_markup=main_markup())

    except Exception as e:

        pass


@router.callback_query(CallbackDataUnsubscribe.filter(), UnSubscribe.article)
async def set_unsubscribe(call: types.CallbackQuery, state: FSMContext, callback_data: CallbackDataUnsubscribe):
    article_id = str(callback_data.action)

    article_id_from_db = session.scalar(select(User).where(User.article_id == article_id))

    article_id_from_db.next_message = None
    session.commit()

    await call.message.answer(f"Вы отписались от обновления по артикулу {callback_data.data}",
                                    reply_markup=main_markup())
    await state.clear()

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from context.set_article import UnSubscribe
from config import redis_client
from buttons.user.main import main_markup, CallbackDataUnsubscribe, create_unsubscribe_markup
from service.get_data_from_redis import get_data_from_redis

router = Router()


@router.message(F.text == '👉 Остановить уведомления')
async def stop_notification(message: types.Message, state: FSMContext):
    try:
        data = await get_data_from_redis(message.from_user.id)

        if data:

            await message.answer(f"Вы подписаны на следующие обновления:",
                                 reply_markup=await create_unsubscribe_markup(data))
            await state.set_state(UnSubscribe.article)

        else:

            await message.answer("Вы пока не подписались на обновления", reply_markup=main_markup())

    except Exception:

        await message.answer("Ошибка!, повторите позднее", reply_markup=main_markup())


@router.callback_query(CallbackDataUnsubscribe.filter(), UnSubscribe.article)
async def set_unsubscribe(call: types.CallbackQuery, state: FSMContext, callback_data: CallbackDataUnsubscribe):
    article_id = str(callback_data.action)

    redis_key = f"subscription:{article_id}"
    redis_client.delete(redis_key)

    await call.message.answer(f"Вы отписались от обновления по артикулу {callback_data.data}",
                              reply_markup=main_markup())
    await state.clear()

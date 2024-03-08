import asyncio
from datetime import datetime, timedelta
from config import session
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from context.set_article import SetArticle
from service.wb import search_article_from_wb
from buttons.user.main import main_markup, subscribe, CallbackDataSubscribe
from data.models import User

router = Router()


@router.message(F.text == '👉 Получить информацию по товару')
async def search_article(message: types.Message, state: FSMContext):
    await message.answer("Введите артикул товара", reply_markup=types.ReplyKeyboardRemove())

    await state.set_state(SetArticle.article)


@router.message(SetArticle.article)
async def get_article(message: types.Message, state: FSMContext):
    await message.answer("Идет поиск...")

    data = await search_article_from_wb(message.text)

    if data:

        try:
            data_from_db = session.query(User).filter(User.article_id == message.text).first()

            if data_from_db:

                pass

            else:

                user = User(
                    user_id=message.from_user.id,
                    time_request=datetime.now().time(),
                    article_id=message.text
                )

                session.add(user)
                session.commit()

        except Exception as e:

            await message.answer(f"Ошибка при добавлении данных! {e}\n"
                                 f"Попробуйте позже", reply_markup=main_markup())
            await state.clear()

        await message.answer("Найдено!")

        await asyncio.sleep(1)

        await message.answer(f"<b>Информация о товаре:</b>\n"
                             f"\n"
                             f"<b>Название:</b> {data['data']['products'][0]['name']}\n"
                             f"<b>Артикул:</b> {data['data']['products'][0]['id']}\n"
                             f"<b>Цена:</b> {data['data']['products'][0]['priceU']/ 100:.2f} RUB\n"
                             f"<b>Цена со скидкой:</b> {data['data']['products'][0]['salePriceU']/ 100:.2f} RUB\n"
                             f"<b>Рейтинг товара:</b> {data['data']['products'][0]['reviewRating']}\n"
                             f"<b>Количество на всех складах:</b> {sum(stock['qty'] for stock in data['data']['products'][0]['sizes'][0]['stocks'])}",
                             parse_mode='HTML', reply_markup=subscribe(data['data']['products'][0]['id']))
        await state.clear()

    else:

        await message.answer("По данному артиклу ничего не найдено", reply_markup=main_markup())

        await state.clear()


@router.callback_query(CallbackDataSubscribe.filter())
async def start_subscribe(call: types.CallbackQuery, callback_data: CallbackDataSubscribe):

    user = session.query(User).filter(User.article_id == str(callback_data.action)).first()

    current_time = datetime.now()

    time_delta = current_time + timedelta(minutes=5)

    user.next_message = time_delta.time()
    session.commit()

    await call.message.answer("Вы успешно подписались на обновления!", reply_markup=main_markup())

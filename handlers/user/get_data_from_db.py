from aiogram import types, Router, F
from config import session
from buttons.user.main import main_markup
from data.models import User
from sqlalchemy import desc

router = Router()


@router.message(F.text == '👉 Получить информацию из БД')
async def get_data(message: types.Message):
    try:

        data = session.query(User).filter(User.user_id == str(message.from_user.id)).order_by(desc(User.id)).limit(5).all()

        if not data:

            await message.answer("База данных пуста", reply_markup=main_markup())

        else:

            text = ("<b>Информация по базе данных</b>\n"
                    "\n")

            for d in data:
                text_from_db = (f"<b>ID пользователя:</b> {d.user_id}\n"
                                f"<b>ID Артикула:</b> {d.article_id}\n"
                                f"<b>Время запроса:</b> {d.time_request.strftime('%H:%M:%S')}\n"
                                f"______________________________\n")
                text += text_from_db

            await message.answer(text, reply_markup=main_markup(), parse_mode="HTML")

    except Exception as e:

        pass

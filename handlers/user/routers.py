from aiogram import Router
from handlers.user.main import router as start_router
from handlers.user.search_article import router as search_router
from handlers.user.stop_notification import router as notification_router
from handlers.user.get_data_from_db import router as get_data_router


user_router = Router()


user_router.include_router(start_router)
user_router.include_router(search_router)
user_router.include_router(notification_router)
user_router.include_router(get_data_router)

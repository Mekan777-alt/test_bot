import os
from data.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv


load_dotenv()

db_name = os.getenv('DBNAME')
db_user = os.getenv('DBUSER')
db_pass = os.getenv('DBPASSWORD')
db_host = os.getenv('DBHOST')
db_port = os.getenv('DBPORT')

db_url = f'postgresql://{db_user}:{db_pass}@db:{db_port}/{db_name}'

engine = create_engine(db_url, echo=False)
Base.metadata.create_all(engine)
session = Session(engine)

token = os.getenv('TOKEN')
bot = Bot(token=token)

dp = Dispatcher(bot=bot, storage=MemoryStorage())

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from tools import admin
from keyboards import kb

db = None
sendel = None

router = Router()  # [1]

@router.message(Command("start"))  # [2]
async def cmd_start(msg: Message):
    if not db.user_exists(msg.from_user.id):
        privilege = "user"
    
        if admin.check(msg.from_user.id):
            privilege = "0"
        
        user_id = db.add_user(
            msg.from_user.id,
            msg.from_user.username,
            privilege)
        
        print("Записан пользователь: " + str(user_id))
    
    await sendel(msg, "Добро пожаловать! Это бот для отслеживания цен на ВБ", kb.start.get())
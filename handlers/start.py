from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums import MessageEntityType

from tools import admin
from tools import parser
from keyboards import kb
from BotDb import Database

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


@router.message(F.entities[...].type == MessageEntityType.URL)
async def url_message_handler(msg: Message):
    if db.user_exists(msg.from_user.id):

        if "wildberries" in msg.text:
            item = parser.get_info_by_url(msg.text)
            if not db.order_exists(item.art, msg.from_user.id):
                db.add_order(msg.from_user.id, item.art, item.name, msg.text, item.price)
                await msg.answer(f"В отслеживание добавлен товар:"+\
                                    f"\nАртикул - {item.art}"+\
                                    f"\nНазвание - {item.name}"+\
                                    f"\nURL - {msg.text}"+\
                                    f"\nЦена - {item.price}",
                                reply_markup=kb.hide.get())
                await msg.delete()
            else:
                item = db.get_order_by_art(item.art, msg.from_user.id)
                await msg.answer(f"Товар уже добавлен в отслеживание:"+\
                                    f"\nАртикул - {item['art']}"+\
                                    f"\nНазвание - {item['name']}"+\
                                    f"\nURL - {item['url']}"+\
                                    f"\nЦена - {item['price']}"+\
                                    f"\nПоследнее обновление {item['last_update']}",
                                reply_markup=kb.item.get())
                await msg.delete()

        else:
            await msg.answer("Неверная ссылка!", reply_markup=kb.hide.get())
            await msg.delete()

    else:
        await msg.answer("Сначала напишите /start", reply_markup=kb.hide.get())
        await msg.delete()


@router.callback_query(F.data == "hide")
async def hide_any_message(call: CallbackQuery):
    await call.message.delete()
    await call.answer()
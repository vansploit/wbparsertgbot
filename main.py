import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import start, settings, tracked
from BotDb import Database
from tools import sendel

db = Database("bot_data.db")

# Запуск бота
async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    for i in [start, settings, tracked]:
        i.db = db
        i.sendel = sendel
    dp.include_routers(start.router, tracked.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
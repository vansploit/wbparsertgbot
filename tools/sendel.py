from aiogram.types import CallbackQuery

user_last_message = {}
async def send_and_delete_msg(msg, answer, keyboard = None):

    if type(msg) is CallbackQuery:
        user_id = msg.from_user.id
        msg = msg.message
    else:
        user_id = msg.from_user.id
    if user_id in user_last_message:
        await user_last_message[user_id].delete()
    if keyboard != None:
        del_msg = await msg.answer(answer, reply_markup = keyboard, parse_mode = 'HTML')
    else:
        del_msg = await msg.answer(answer, parse_mode = 'HTML')
    user_last_message[user_id] = del_msg
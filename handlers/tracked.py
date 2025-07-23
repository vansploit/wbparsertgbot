from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from tools import admin
from keyboards import kb

db = None
sendel = None

router = Router()

class TrackedState(StatesGroup):
    pages = State()


async def _update_tracked_page(call: CallbackQuery, state: FSMContext, page_change: int = 0):
    data = await state.get_data()
    kb.tracked.clear()
    kb.pages.clear()
    
    pages_list = data["pages_list"]
    cur_page = data["cur_page"] + page_change
    
    if 0 <= cur_page < len(pages_list):
        for num, order in enumerate(pages_list[cur_page]):
            kb.tracked.add((f"#{order['id']} {order['name']}", "order_" + str(num)))
        
        kb.tracked.adjust(1)
        kb.pages.add(
            ("##", "##") if cur_page == 0 else ("<<", "page_prev"),
            ("[назад]", "back"),
            ("##", "##") if cur_page == len(pages_list)-1 else (">>", "page_next")
        )
        kb.pages.adjust(3)
        kb.tracked.attach(kb.pages.builder)
        
        await state.update_data(cur_page=cur_page)
        await sendel(call, "Вот список ваших отслеживаний:\n", kb.tracked.get())

@router.callback_query(F.data == "tracked")
async def tracked_handler(call: CallbackQuery, state: FSMContext):
    orders = db.get_user_orders(call.from_user.id)
    pages_list = [orders[i:i + 5] for i in range(0, len(orders), 5)]
    
    await state.update_data(pages_list=pages_list, cur_page=0)
    await state.set_state(TrackedState.pages)
    await _update_tracked_page(call, state)

@router.callback_query(TrackedState.pages, F.data == "page_prev")
async def tracked_page_prev(call: CallbackQuery, state: FSMContext):
    await _update_tracked_page(call, state, -1)

@router.callback_query(TrackedState.pages, F.data == "page_next")
async def tracked_page_next(call: CallbackQuery, state: FSMContext):
    await _update_tracked_page(call, state, 1)
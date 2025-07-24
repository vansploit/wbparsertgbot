from .MyKeyboard import kb
from .MyKeyboard import SubKb

item = SubKb()

item.add(
	("История цен","price_history*"),
	("Перестать отслеживать", "stop_tracking"),
	("Выход", "exit")
	)
item.adjust(1)

kb.add_child("item", item)
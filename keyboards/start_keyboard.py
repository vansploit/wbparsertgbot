from .MyKeyboard import kb
from .MyKeyboard import SubKb

start = SubKb()

start.add(
           ("Отслеживаемое", "tracked"),
           ("Настройки", "settings"))
           
start.adjust(1,1)

kb.add_child("start", start)
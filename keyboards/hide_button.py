from .MyKeyboard import kb
from .MyKeyboard import SubKb

hidebutton = SubKb()

hidebutton.add(("Скрыть", "hide"))

kb.add_child("hide", hidebutton)
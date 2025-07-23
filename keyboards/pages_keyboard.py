from .MyKeyboard import kb
from .MyKeyboard import SubKb

pages = SubKb()

kb.add_child("pages", pages)
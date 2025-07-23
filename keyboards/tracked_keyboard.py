from .MyKeyboard import kb
from .MyKeyboard import SubKb

tracked = SubKb()

kb.add_child("tracked", tracked)
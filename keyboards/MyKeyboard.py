from aiogram.utils.keyboard import InlineKeyboardBuilder as InlineBuilder
from aiogram.types import InlineKeyboardButton as InlineButton

class KB:
    
    def __init__(self):
        self._children = {}  # Словарь для хранения дочерних объектов

    def add_child(self, name, child_obj):
        setattr(self, name, child_obj)
        self._children[name] = child_obj
            
           
class SubKb:

    def __init__(self):
        self.builder = InlineBuilder()
        
    @classmethod
    def add_attr(cls, name, value):
        setattr(cls, name, value)
        
    def adjust(self, *args):
        self.builder.adjust(*args)
        
    def attach(self, builder):
        self.builder.attach(builder)
        
    def get(self):
        return self.builder.as_markup(resize_keyboard=True)
    
    def add(self, *args):
        for button in args:
            self.builder.add(InlineButton(
                    text=button[0],
                    callback_data=button[1]))
                    
    def clear(self):
        self.builder = InlineBuilder()
                    
kb = KB()
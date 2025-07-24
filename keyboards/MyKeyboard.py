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
        self.adjust = None
        self.buttons = []
        
    @classmethod
    def add_attr(cls, name, value):
        setattr(cls, name, value)
        
    def adjust(self, *args):
        self.adjust(*args)
        
    def attach(self, buttons):
        for button in buttons:
            self.buttons.append(button)
        
    def get(self):
        for button in self.buttons:
            self.builder.add(InlineButton(
                    text=button[0],
                    callback_data=button[1]))
        if self.adjust != None:
            self.builder.adjust(self.adjust)
        return self.builder.as_markup(resize_keyboard=True)
    
    def add(self, *args):
        for button in args:
            self.buttons.append(button)
                    
    def clear(self):
        self.builder = InlineBuilder()

    def set_payload(self, payload):
        temp_lst = []
        for i in self.buttons:
            if "*" in i[1]:
                temp_lst.append(i[0], i[1]+"_"+payload)
            else:
                temp_lst.append(i)
        self.buttons = temp_lst

    def reorder_buttons(self, order):
        # Преобразуем порядок в индексы (отнимаем 1, так как индексы начинаются с 0)
        indices = [int(char) - 1 for char in str(order)]
        # Создаем новый список, переставляя элементы согласно новым индексам
        self.buttons = [self.buttons[i] for i in indices]
                    
kb = KB()
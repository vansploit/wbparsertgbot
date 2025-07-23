from .MyKeyboard import kb
import os
import importlib

# Получаем список всех .py файлов в пакете (кроме __init__.py)
package_dir = os.path.dirname(__file__)
modules = [
    f[:-3]  # Убираем '.py'
    for f in os.listdir(package_dir)
    if f.endswith('.py') and not f.startswith('_')
]

# Динамически импортируем каждый модуль и добавляем его в глобальное пространство
for module_name in modules:
    module = importlib.import_module(f".{module_name}", package=__package__)
    globals()[module_name] = module

# Опционально: можно добавить __all__ для from ... import *
__all__ = modules
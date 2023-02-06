from pathlib import Path
from os import listdir
from importlib import import_module

path_parent = Path('./app/models')

for module in listdir(path_parent):
    if 'model' in module:
        import_module(
            f'app.models.{module[:-3]}'
        )

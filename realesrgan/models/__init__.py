import importlib
from basicsr.utils import scandir
from os import path as osp

# automatically scan and import models modules for registry
# scan all the files that end with '_model.py' under the models folder
model_folder = osp.dirname(osp.abspath(__file__))
model_filenames = [osp.splitext(osp.basename(v))[0] for v in scandir(model_folder) if v.endswith('_model.py')]
# import all the models modules
_model_modules = [importlib.import_module(f'realesrgan.models.{file_name}') for file_name in model_filenames]

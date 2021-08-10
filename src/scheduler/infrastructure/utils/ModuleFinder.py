import glob
import importlib
import os

from injector import inject

from infrastructure.dependency.scopes import ISingleton
from infrastructure.utils.Utils import Utils
from models.configs.ApplicationConfig import ApplicationConfig


class ModuleFinder(ISingleton):
    @inject
    def __init__(self, application_config: ApplicationConfig):
        self.application_config = application_config
        self.root_directory = application_config.root_directory
        self.modules = []

        self.get_indexes = lambda module_name, modules: [i for (module, i) in zip(modules, range(len(modules))) if
                                                         module["module_name"] == module_name]
        self.find_all_modules(self.root_directory)

    def get_file_name(self, file):
        file_splits = Utils.path_split(file)
        file_name = file_splits[len(file_splits) - 1]
        file_name_without_extension = file_name[0:(len(file_name) - 3)]
        return file_name_without_extension

    @staticmethod
    def find_sub_folders(directory):
        for name in os.listdir(directory):
            sub_folder = os.path.join(directory, name)
            if os.path.isdir(sub_folder) and not name.startswith('.') and not name.startswith('_') and name != 'files':
                yield sub_folder
                for folder in ModuleFinder.find_sub_folders(sub_folder):
                    yield folder

    def find_all_modules(self, folder):
        folder_path = os.path.join(folder)
        folders = self.find_sub_folders(folder_path)
        for folder in folders:
            files = glob.glob(folder + '/*.py')
            for file in files:
                module = {}
                file_name = self.get_file_name(file=file)
                module_path = os.path.join(folder, file_name)
                module_address = module_path.replace(self.root_directory, '')[1:].replace('\\', '.').replace('/', '.')
                module['module_name'] = file_name
                module['file_path'] = file
                module['module_path'] = module_path
                module['module_address'] = module_address
                self.modules.append(module)

    def import_modules(self, included_modules=None, excluded_modules=None):
        for module in self.modules:
            base_module_folder = \
                module['module_path'].replace(self.application_config.root_directory + '\\', '')
            if ((excluded_modules is None) or (
            not any(base_module_folder.startswith(item) for item in excluded_modules))) and (
                    (included_modules is None) or (included_modules is not None and any(
                    base_module_folder.startswith(item) for item in included_modules))):
                module_address = module["module_address"]
                importlib.import_module(module_address)

    def get_module(self, name_of_module):
        indexes = self.get_indexes(name_of_module, self.modules)
        if indexes is not None and len(indexes) > 0:
            if len(indexes) == 1:
                module_address = self.modules[indexes[0]]["module_address"]
                module = importlib.import_module(module_address)
                return module
        else:
            raise Exception("Modules not found")

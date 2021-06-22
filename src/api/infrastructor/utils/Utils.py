import glob
import inspect
from multiprocessing.process import current_process
import os
import re
import sys
from datetime import datetime


class Utils:
    @staticmethod
    def object_as_dict(obj):
        dic = dict()
        for c in inspect(obj).mapper.column_attrs:
            val = getattr(obj, c.key)
            if isinstance(val, datetime):
                val = val.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            dic[c.key] = val
        return dic

    @staticmethod
    def replace_last(source_string, replace_what, replace_with):
        head, _sep, tail = source_string.rpartition(replace_what)
        return head + replace_with + tail

    @staticmethod
    def to_snake_case(name):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        name = re.sub('__([A-Z])', r'_\1', name)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
        return name.lower()

    @staticmethod
    def get_config_name(class_name):
        replace_what = 'Config'
        replace_with = ''
        replaced_name = Utils.replace_last(source_string=class_name, replace_what=replace_what,
                                           replace_with=replace_with)
        snaked_case = Utils.to_snake_case(replaced_name)
        result = snaked_case.upper()
        return result

    @staticmethod
    def find_sub_folders(directory):
        for name in os.listdir(directory):
            sub_folder = os.path.join(directory, name)
            if os.path.isdir(sub_folder) and not name.startswith('.') and not name.startswith(
                    '__') and not name.startswith(
                '__') and name != 'dao' and name != 'alembic' and name != 'unittests' and name != 'files':
                yield sub_folder
                for folder in Utils.find_sub_folders(sub_folder):
                    yield folder

    @staticmethod
    def dict_to_array(module_dict):
        members = inspect.getmembers(module_dict, lambda a: not (inspect.isroutine(a)))
        for key, value in members:
            temp = [key, value]
            if inspect.isclass(value):
                yield temp

    @staticmethod
    def get_modules(folders) -> ([], []):
        module_list = []
        module_attr_list = []
        for folder in folders:
            sys.path.append(folder)
            files = glob.glob(folder + '/*.py')
            for file in files:
                file_splits = file.split('/')
                if len(file_splits) == 1:
                    file_splits = file.split('\\')
                file_name = file_splits[len(file_splits) - 1]
                file_name_without_extension = file_name[0:(len(file_name) - 3)]
                module = __import__(file_name_without_extension)
                for module_attr in Utils.dict_to_array(module):
                    attr_name = module_attr[0]
                    attr = getattr(module, attr_name)
                    if not inspect.isabstract(
                            module_attr[1]) and attr not in module_list and attr_name not in module_attr_list:
                        module_list.append(attr)
                        module_attr_list.append(module_attr[0])
        return module_list, module_attr_list

    @staticmethod
    def get_connection_string(database_config):
        if database_config.driver is not None and database_config.driver != '':
            driver = database_config.driver.replace(' ', '+')
        driver_string = ''
        connection_type = ''
        if database_config.type == 'MSSQL':
            driver_string = f'?driver={driver}'
            connection_type = 'mssql+pyodbc'
        elif database_config.type == 'POSTGRESQL':
            connection_type = 'postgresql'
        connection_string = f'{connection_type}://{database_config.username}:{database_config.password}@{database_config.host}:{database_config.port}/{database_config.database}{driver_string}'
        return connection_string

    def get_process_info():
    
        print(f"Application : {application_name}")
        print(f"Process Name : {current_process().name}")
        print(f"Pid : {os.getpid()}")
        print(f"Parent Pid : {os.getppid()}")
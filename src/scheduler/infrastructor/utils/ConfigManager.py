import os
import re
import sys

import yaml
from infrastructor.utils.Utils import Utils
from models.configs.BaseConfig import BaseConfig


class ConfigManager:
    def __init__(self, root_directory: str) -> None:
        # Create an empty list with items of type T
        self.configs = self.__get_configs(root_directory)

    def get_all(self):
        return self.configs

    def get(self, generic_type):
        for config in self.configs:
            config_type = config.get("type")
            if config_type is generic_type:
                return config.get("instance")

    def set(self, generic_type, instance_property, property_value):
        config_instance=self.get(generic_type=generic_type)
        setattr(config_instance, instance_property, property_value)

    def empty(self) -> bool:
        return not self.items

    @staticmethod
    def to_snake_case(name):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        name = re.sub('__([A-Z])', r'_\1', name)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
        return name.lower()

    @staticmethod
    def __get_configs(root_directory) -> []:
        config_path = os.path.join(root_directory, "models", "configs")
        sys.path.append(config_path)
        module_list, module_attr_list = Utils.get_modules([config_path])
        environment =  os.getenv('PYTHON_ENVIRONMENT', None)
        config_path = "application.yml"
        if environment is not None:
            config_path_splitted = "application.yml".split('.')
            config_path = f'{config_path_splitted[0]}.{environment}.{config_path_splitted[1]}'
        with open(os.path.join(root_directory, config_path), 'r') as yml_file:
            loaded_configs = yaml.load(yml_file, Loader=yaml.FullLoader)
        configs = []
        for config in BaseConfig.__subclasses__():
            config_instance = config()
            class_name = Utils.get_config_name(config_instance.__class__.__name__)
            class_properties = [a for a in dir(config_instance) if not (a.startswith('_'))]
            for prop in class_properties:
                property_name = prop.upper()
                if class_name in loaded_configs:
                    loaded_config=loaded_configs[class_name]
                    if property_name in loaded_config:
                        config_value = loaded_config[property_name]
                    elif property_name == 'ROOT_DIRECTORY':
                        config_value = root_directory
                    else:
                        config_value = None
                else:
                    config_value = None

                environment_name = f'{class_name}_{property_name}'
                property_value = os.getenv(environment_name, config_value)
                setattr(config_instance, prop, property_value)
            configs.append({"type": config, "instance": config_instance})
        return configs

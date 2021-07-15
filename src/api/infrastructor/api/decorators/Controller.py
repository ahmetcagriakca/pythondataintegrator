import os
import sys

from IocManager import IocManager
from infrastructor.api.decorators.Endpoint import endpoint
from infrastructor.utils.Utils import Utils
from models.configs.ApplicationConfig import ApplicationConfig


def controller(namespace=None, route=None, exclude=None):
    if exclude is None:
        exclude = []
    white_list = ['get', 'post', 'put', 'delete']

    def find_namespace(cls):
        namespace_name = get_namespace_name(cls)
        founded_namespace=None
        for api_namespace in IocManager.api.namespaces:
            if api_namespace.name == namespace_name:
                founded_namespace = api_namespace
                break
        else:
            founded_namespace = IocManager.api.namespace(namespace_name,
                                                         description=f'{namespace_name} endpoints',
                                                         path=f'/api/{namespace_name}')
        return founded_namespace

    def get_namespace_name(cls):

        root_directory = IocManager.config_manager.get(ApplicationConfig).root_directory
        controllers_path = os.path.join(root_directory, 'controllers')
        module_name = cls.__module__
        module_path = sys.modules[module_name].__file__
        namespace_folder = module_path.replace(f'{controllers_path}\\', '')
        split_namespace = Utils.path_split(namespace_folder)
        name=split_namespace[0].title()
        return name

    def find_route(cls):
        namespace_name = get_namespace_name(cls)
        route_path = cls.__name__.replace('Resource', '').replace(namespace_name, '')
        return f'/{route_path}' if route_path is not None and route_path!='' else ''

    def decorate(cls):
        controller_namespace = namespace

        if controller_namespace is None:
            controller_namespace = find_namespace(cls)

        controller_route = route
        if controller_route is None:
            controller_route = find_route(cls)

        decorator = endpoint(namespace=controller_namespace)
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)) and attr not in exclude and attr in white_list:
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return controller_namespace.route(controller_route)(cls)

    return decorate

from injector import inject
import os

from IocManager import IocManager
from infrastructure.dependency.scopes import IScoped
from infrastructure.utils.ModuleFinder import ModuleFinder
from models.configs.ApplicationConfig import ApplicationConfig


class GenerateCommand(IScoped):
    @inject
    def __init__(self,
                 application_config: ApplicationConfig,
                 module_finder: ModuleFinder):
        self.application_config = application_config
        self.module_finder = module_finder

    def check_path_exist(self, folder, file):
        path= os.path.join(self.application_config.root_directory, folder, file)
        return os.path.exists(path)

    def create_folder_if_not_exist(self, folder):
        os.path.join(self.application_config.root_directory, folder)
        if not os.path.exists(folder):
            os.makedirs(folder)

    def create_old_file(self, file_path, old_file_path):
        with open(file_path, "r") as outfile:
            content = outfile.read()

        with open(old_file_path, "w") as outfile:
            outfile.write(content)

    def create_file(self, folder, file_name, content, file_extension='.py'):
        self.create_folder_if_not_exist(folder)
        file_path = '/'.join([folder, f'{file_name}{file_extension}'])
        if self.check_path_exist(folder, f'{file_name}{file_extension}'):
            old_file_path = '/'.join([folder, f'{file_name}_old{file_extension}'])
            self.create_old_file(file_path=file_path, old_file_path=old_file_path)

        with open(file_path, "w") as outfile:
            outfile.write(content.strip()+'\n')

    def create_command_file(self, command_name: str, command_folder_path: str, has_request):
        command_file_name = f"{command_name}Command"
        command_namespace = command_folder_path.replace('/', '.')
        request_namespace = '''
'''
        request_attr = ''
        if has_request:
            request_namespace = f'from {command_namespace}.{command_name}Request import {command_name}Request'
            request_attr = f'request: {command_name}Request = None'
        command_content = \
f'''
from dataclasses import dataclass
from infrastructure.cqrs.ICommand import ICommand
{request_namespace}


@dataclass
class {command_name}Command(ICommand):
    # TODO:Command attributes
    {request_attr}
    pass
        '''
        self.create_file(folder=command_folder_path, file_name=command_file_name, content=command_content)

    def create_command_handler_file(self, command_name: str, command_folder_path: str):
        command_handler_file_name = f"{command_name}CommandHandler"
        command_namespace = command_folder_path.replace('/', '.')
        command_handler_content = \
f'''
from injector import inject
from {command_namespace}.{command_name}Command import {command_name}Command
from infrastructure.cqrs.ICommandHandler import ICommandHandler


class {command_name}CommandHandler(ICommandHandler[{command_name}Command]):
    @inject
    def __init__(self,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass
        
    def handle(self, command: {command_name}Command):
        # TODO:Handle command operation
        pass
'''
        self.create_file(folder=command_folder_path, file_name=command_handler_file_name,
                         content=command_handler_content)

    def create_command_request_file(self, command_name: str, command_folder_path: str):
        command_request_file_name = f"{command_name}Request"
        # command_request_file = "/".join([command_folder_path, command_request_file_name])
        command_request_content = \
            f'''
            from domain.common.decorators.requestclass import requestclass


@requestclass
class {command_name}Request:
    # TODO:Request attributes
    pass
    '''
        self.create_file(folder=command_folder_path, file_name=command_request_file_name,
                         content=command_request_content)

    def generate(self, domain, name, has_request=False):
        base_folder = "domain"
        domain_folder = f"{domain}"
        command_folder = f"{name}"
        command_folder_path = "/".join([base_folder, domain_folder, command_folder])

        self.create_command_file(command_name=name, command_folder_path=command_folder_path, has_request=has_request)
        self.create_command_handler_file(command_name=name, command_folder_path=command_folder_path)
        if has_request:
            self.create_command_request_file(command_name=name, command_folder_path=command_folder_path)


root_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))
application_config = ApplicationConfig(root_directory=root_directory)
module_finder = ModuleFinder(application_config=application_config)
generate_command = GenerateCommand(application_config=application_config, module_finder=module_finder)
# generate_command.generate('connection', 'CreateConnectionFile', has_request=True)
# IocManager.initialize()
# IocManager.injector.get(GenerateCommand).generate('connection', 'CreateConnectionFile')

generate_command.generate('operation', 'DeleteDataOperation', has_request=False)
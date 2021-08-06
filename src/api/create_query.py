from injector import inject
import os

from FolderManager import FolderManager
from infrastructure.dependency.scopes import IScoped
from infrastructure.utils.ModuleFinder import ModuleFinder
from models.configs.ApplicationConfig import ApplicationConfig


class GenerateQuery(IScoped):
    @inject
    def __init__(self,
                 application_config: ApplicationConfig,
                 module_finder: ModuleFinder,
                 folder_manager: FolderManager):
        self.folder_manager = folder_manager
        self.application_config = application_config
        self.module_finder = module_finder

    def check_path_exist(self, folder, file):
        path = os.path.join(self.application_config.root_directory, folder, file)
        return os.path.exists(path)

    def create_folder_if_not_exist(self, folder):
        os.path.join(self.application_config.root_directory, folder)
        if not os.path.exists(folder):
            os.makedirs(folder)

    def create_file(self, folder, file_name, content, file_extension='.py'):
        self.create_folder_if_not_exist(folder)
        file_path = '/'.join([folder, f'{file_name}{file_extension}'])

        with open(file_path, "w") as outfile:
            outfile.write(content.strip() + '\n')

    def create_query_file(self, query_name: str, query_folder_path: str, is_list: bool = True,
                          has_paging: bool = True, ):
        file_name = f"{query_name}Query"
        base_namespace = query_folder_path.replace('/', '.')
        request_namespace = f'from {base_namespace}.{query_name}Request import {query_name}Request'
        response_namespace = f'from {base_namespace}.{query_name}Response import {query_name}Response'
        request_attr = f'request: {query_name}Request = None'
        content = \
            f'''from dataclasses import dataclass
from infrastructure.cqrs.IQuery import IQuery
{request_namespace}
{response_namespace}


@dataclass
class {query_name}Query(IQuery[{query_name}Response]):
    {request_attr}
        '''
        self.create_file(folder=query_folder_path, file_name=file_name, content=content)

    def create_request_file(self, query_name: str, query_folder_path: str, is_list: bool = True,
                            has_paging: bool = True, ):
        file_name = f"{query_name}Request"
        paging_parent = "(PagingParameter, OrderByParameter)" if has_paging else ""
        content = \
            f'''
from domain.common.decorators.requestclass import requestclass


@requestclass
class {query_name}Request{paging_parent}:
    # TODO:Request attributes
    pass
    '''
        self.create_file(folder=query_folder_path, file_name=file_name,
                         content=content)

    def create_dto_file(self, query_name: str, query_folder_path: str, is_list: bool = True,
                        has_paging: bool = True):
        file_name = f"{query_name}Dto"

        content = \
            f'''
from domain.common.decorators.dtoclass import dtoclass


@dtoclass
class {query_name}Dto:
    # TODO:Dto attributes
    pass
    '''
        self.create_file(folder=query_folder_path, file_name=file_name,
                         content=content)

    def create_response_file(self, query_name: str, query_folder_path: str, is_list: bool, has_paging: bool):
        query_request_file_name = f"{query_name}Response"

        base_namespace = query_folder_path.replace('/', '.')
        dto_namespace = f'from {base_namespace}.{query_name}Dto import {query_name}Dto'
        if is_list:
            if has_paging:
                attributes = \
                    f'''    Data: List[{query_name}Dto] = None
    PageNumber: int = None
    PageSize: int = None
    Count: int = None'''
            else:
                attributes = f"\tData: List[{query_name}Dto] = None"
        else:
            attributes = f"\tData: {query_name}Dto = None"
        content = \
            f'''
from typing import List
from domain.common.decorators.responseclass import responseclass
{dto_namespace}


@responseclass
class {query_name}Response:
{attributes}
    '''
        self.create_file(folder=query_folder_path, file_name=query_request_file_name,
                         content=content)

    def create_specifications_file(self, query_name: str, query_folder_path: str, is_list: bool = True,
                                   has_paging: bool = True, ):
        file_name = f"{query_name}Specifications"

        base_namespace = query_folder_path.replace('/', '.')
        query_namespace = f'from {base_namespace}.{query_name}Query import {query_name}Query'
        orderable = {}
        pageable = {}
        if is_list:
            if has_paging:
                orderable[
                    'Namespace'] = f'from domain.common.specifications.OrderBySpecification import OrderBySpecification\n'
                pageable[
                    'Namespace'] = f'from domain.common.specifications.PagingSpecification import PagingSpecification\n'
        content = ''
        content += 'from injector import inject\n'
        content += 'from sqlalchemy.orm import Query\n'
        content += 'from infrastructure.dependency.scopes import IScoped\n'
        content += f'{query_namespace}\n'
        if has_paging:
            content += orderable['Namespace']
            content += '\n'
            content += pageable['Namespace']
            content += '\n'
        content += '\n'
        content += \
            f'''
class {query_name}Specifications(IScoped):
    @inject
    def __init__(self,\n'''
        if has_paging:
            content += f'''                 order_by_specification: OrderBySpecification,\n'''
            content += f'''                 paging_specification: PagingSpecification,\n'''
        content += f'''                 ):\n'''
        if has_paging:
            content += f'''        self.paging_specification = paging_specification\n'''
            content += f'''        self.order_by_specification = order_by_specification\n'''
        else:
            content += f'''        pass\n'''
        content += \
            f'''
    def __specified_query(self, query: {query_name}Query, data_query: Query) -> Query:
        specified_query = data_query 
        # TODO:specify query
        return specified_query
        
    def specify(self, data_query: Query, query: {query_name}Query) -> Query:
        data_query = self.__specified_query(query=query, data_query=data_query)\n'''
        if has_paging:
            content += f'''
        order_by = self.order_by_specification.specify(order_by_parameter=query.request)
        if order_by is not None:
            data_query = data_query.order_by(order_by)

        page_size, offset = self.paging_specification.specify(paging_parameter=query.request)
        if page_size is not None:
            data_query = data_query.limit(page_size)
        if offset is not None:
            data_query = data_query.offset(offset)\n'''
        content += '''        return data_query\n'''

        content += f'''
    def count(self, query: {query_name}Query, data_query: Query) -> Query:
        return self.__specified_query(query=query, data_query=data_query).count()
    '''
        self.create_file(folder=query_folder_path, file_name=file_name,
                         content=content)

    def create_mapping_file(self, query_name: str, query_folder_path: str, is_list: bool = True,
                            has_paging: bool = True,
                            dao={}):
        file_name = f"{query_name}Mapping"
        base_namespace = query_folder_path.replace('/', '.')
        dto_namespace = f'from {base_namespace}.{query_name}Dto import {query_name}Dto'
        content = \
            f'''
from typing import List
{dto_namespace}
{dao['Namespace']}


class {query_name}Mapping:
    @staticmethod
    def to_dto(entity: {dao['Name']}) -> {query_name}Dto:
        dto = {query_name}Dto()
        return dto

    @staticmethod
    def to_dtos(entities: List[{dao['Name']}]) -> List[{query_name}Dto]:
        result: List[{query_name}Dto] = []
        for entity in entities:
            dto = {query_name}Mapping.to_dto(entity=entity)
            result.append(dto)
        return result'''
        self.create_file(folder=query_folder_path, file_name=file_name,
                         content=content)

    def create_query_handler_file(self, query_name: str, query_folder_path: str, is_list: bool = True,
                                  has_paging: bool = True,
                                  dao={}):
        file_name = f"{query_name}QueryHandler"
        base_namespace = query_folder_path.replace('/', '.')
        query_namespace = f'from {base_namespace}.{query_name}Query import {query_name}Query'
        mapping_namespace = f'from {base_namespace}.{query_name}Mapping import {query_name}Mapping'
        request_namespace = f'from {base_namespace}.{query_name}Request import {query_name}Request'
        response_namespace = f'from {base_namespace}.{query_name}Response import {query_name}Response'
        specifications_namespace = f'from {base_namespace}.{query_name}Specifications import {query_name}Specifications'
        content = \
            f'''
from injector import inject
{mapping_namespace}
{query_namespace}
{response_namespace}
{specifications_namespace}
from infrastructure.cqrs.IQueryHandler import IQueryHandler
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
{dao['Namespace']}


class {query_name}QueryHandler(IQueryHandler[{query_name}Query], IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 specifications: {query_name}Specifications):
        self.repository_provider = repository_provider
        self.specifications = specifications

    def handle(self, query: {query_name}Query) -> {query_name}Response:
        result = {query_name}Response()
        repository = self.repository_provider.get({dao['Name']})
        data_query = repository.table\n'''
        if has_paging:
            content += f'''
        result.Count = self.specifications.count(query=query, data_query=data_query)

        result.PageNumber = query.request.PageNumber
        result.PageSize = query.request.PageSize\n'''

        content += \
            f'''        data_query = self.specifications.specify(query=query, data_query=data_query)\n'''
        if is_list:
            content += \
                f'''        result.Data = {query_name}Mapping.to_dtos(data_query)\n'''
        else:
            content += \
                f'''        result.Data = {query_name}Mapping.to_dto(data_query)\n'''
        content += \
            f'''        return result\n'''
        self.create_file(folder=query_folder_path, file_name=file_name,
                         content=content)

    def generate(self, base_folder, domain, name, has_request=False, is_list: bool = True,
                 has_paging: bool = True,
                 dao={}):

        domain_folder = f"{domain}"
        query_folder = f"{name}"
        query_folder_path = "/".join([base_folder, domain_folder, query_folder])

        self.folder_manager.start_copy(query_folder_path)

        self.create_request_file(query_name=name, query_folder_path=query_folder_path, is_list=is_list,
                                 has_paging=has_paging)
        self.create_dto_file(query_name=name, query_folder_path=query_folder_path, is_list=is_list,
                             has_paging=has_paging)
        self.create_response_file(query_name=name, query_folder_path=query_folder_path, is_list=is_list,
                                  has_paging=has_paging)
        self.create_query_file(query_name=name, query_folder_path=query_folder_path, is_list=is_list,
                               has_paging=has_paging)
        self.create_specifications_file(query_name=name, query_folder_path=query_folder_path, is_list=is_list,
                                        has_paging=has_paging)

        self.create_mapping_file(query_name=name, query_folder_path=query_folder_path, is_list=is_list,
                                 has_paging=has_paging, dao=dao)
        self.create_query_handler_file(query_name=name, query_folder_path=query_folder_path, is_list=is_list,
                                       has_paging=has_paging, dao=dao)


root_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))
folder_manager = FolderManager(root_directory)
application_config = ApplicationConfig(root_directory=root_directory)
module_finder = ModuleFinder(application_config=application_config)
generate_query = GenerateQuery(application_config=application_config, module_finder=module_finder,
                               folder_manager=folder_manager)
# generate_query.generate('connection', 'CreateConnectionFile', has_request=True)
# IocManager.initialize()
# IocManager.injector.get(GenerateQuery).generate('connection', 'CreateConnectionFile')
base_dir = "domain"
domain = "connection"
query = f"CheckDatabaseConnection"
is_list = True
has_paging = False
dao = {
    'Name': 'Log',
    'Namespace': 'from models.dao.common.Log import Log'
}
generate_query.generate(base_dir, domain, query, is_list=is_list, has_paging=has_paging, dao=dao)

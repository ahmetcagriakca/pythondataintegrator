import os

from generator.FileManager import FileManager
from generator.FolderManager import FolderManager
from generator.QueryGenerator import QueryGenerator
from generator.domain.DaoGenerateConfig import DaoGenerateConfig
from generator.domain.QueryGenerateConfig import QueryGenerateConfig
from infrastructure.utils.ModuleFinder import ModuleFinder
from models.configs.ApplicationConfig import ApplicationConfig

root_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))
application_config = ApplicationConfig(root_directory=root_directory)
folder_manager = FolderManager(application_config=application_config)
file_manager = FileManager(application_config=application_config)
module_finder = ModuleFinder(application_config=application_config)
query_generator = QueryGenerator(application_config=application_config, module_finder=module_finder,
                             folder_manager=folder_manager,
                             file_manager=file_manager)
config = QueryGenerateConfig(
    base_directory="domain",
    domain="dashboard",
    name="GetSourceDataAffectedRowWidget",
    dao=DaoGenerateConfig(name='DataOperationJobExecutionIntegration', namespace='from models.dao.operation.DataOperationJobExecutionIntegration import DataOperationJobExecutionIntegration'),
    is_list=False,
    has_paging=False
)
query_generator.generate(generate_config=config)

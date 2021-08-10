import os
from multiprocessing.process import current_process

from injector import singleton, Injector, threadlocal, Binder
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from infrastructure.dependency.scopes import ISingleton, IScoped
from infrastructure.logging.ConsoleLogger import ConsoleLogger
from infrastructure.utils.ConfigManager import ConfigManager
from infrastructure.utils.ModuleFinder import ModuleFinder
from models.configs.ApplicationConfig import ApplicationConfig
from models.configs.DatabaseConfig import DatabaseConfig
from models.configs.ProcessRpcServerConfig import ProcessRpcServerConfig


class IocManager:
    binder: Binder = None
    process_service = None
    config_manager: ConfigManager = None
    injector: Injector = None
    Base = declarative_base(metadata=MetaData(schema='Common'))

    @staticmethod
    def initialize():
        logger = ConsoleLogger()
        logger.info(f"Application initialize started")
        root_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))
        IocManager.configure_startup(root_directory)

    @staticmethod
    def set_process_service(process_service=None):
        IocManager.process_service = process_service

    # wrapper required for dependency
    @staticmethod
    def configure_startup(root_directory):
        # Importing all modules for dependency
        application_config = ApplicationConfig(root_directory=root_directory)
        module_finder = ModuleFinder(application_config)
        module_finder.import_modules(excluded_modules=['unittests'])

        # Configuration initialize
        IocManager.config_manager = ConfigManager(root_directory)
        IocManager.set_database_application_name()
        IocManager.injector = Injector(IocManager.configure)
        IocManager.process_info()

    @staticmethod
    def set_database_application_name():
        application_config = IocManager.config_manager.get(ApplicationConfig)
        database_config: DatabaseConfig = IocManager.config_manager.get(DatabaseConfig)
        if database_config.application_name is None:
            process_info = IocManager.get_process_info()
            hostname = os.getenv('HOSTNAME', '')
            IocManager.config_manager.set(ApplicationConfig, "hostname", hostname)
            IocManager.config_manager.set(DatabaseConfig, "application_name",
                                          f"{application_config.name}-({process_info})")

    @staticmethod
    def run():
        process_service = IocManager.process_service()
        process_rpc_server_config: ProcessRpcServerConfig = IocManager.config_manager.get(ProcessRpcServerConfig)
        process_service.initialize(process_rpc_server_config=process_rpc_server_config)

    @staticmethod
    def configure(binder: Binder):
        IocManager.binder = binder

        for config in IocManager.config_manager.get_all():
            binder.bind(
                config.get("type"),
                to=config.get("instance"),
                scope=singleton,
            )

        for singletonScope in ISingleton.__subclasses__():
            binder.bind(
                singletonScope,
                to=singletonScope,
                scope=singleton,
            )

        for scoped in IScoped.__subclasses__():
            binder.bind(
                scoped,
                to=scoped,
                scope=threadlocal,
            )

    @staticmethod
    def get_process_info():
        return f"{current_process().name} ({os.getpid()},{os.getppid()})"

    @staticmethod
    def process_info():
        logger = ConsoleLogger()
        application_config: ApplicationConfig = IocManager.config_manager.get(ApplicationConfig)
        hostname = f'-{application_config.hostname}' if (
                    application_config.hostname is not None and application_config.hostname != '') else ''
        logger.info(f"Application : {application_config.name}{hostname}")

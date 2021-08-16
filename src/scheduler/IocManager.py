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
from models.configs.SchedulerRpcServerConfig import SchedulerRpcServerConfig


class IocManager:
    binder: Binder = None
    job_scheduler = None
    scheduler_service = None
    config_manager = None
    injector: Injector = None
    Base = declarative_base(metadata=MetaData(schema='Common'))

    @staticmethod
    def initialize():
        logger = ConsoleLogger()
        logger.info(f"Application initialize started")
        root_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))
        IocManager.configure_startup(root_directory)

    @staticmethod
    def set_job_scheduler(job_scheduler=None):
        IocManager.job_scheduler = job_scheduler

    @staticmethod
    def set_scheduler_service(scheduler_service=None):
        IocManager.scheduler_service = scheduler_service

    # wrapper required for dependency
    @staticmethod
    def configure_startup(root_directory):
        # Importing all modules for dependency
        application_config = ApplicationConfig(root_directory=root_directory)
        module_finder = ModuleFinder(application_config)
        dao_path = os.path.join('models','dao','aps','ApSchedulerJobsTable')
        module_finder.import_modules(excluded_modules=[dao_path])

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
        job_scheduler = IocManager.injector.get(IocManager.job_scheduler)
        job_scheduler.run()
        scheduler_service = IocManager.scheduler_service()
        scheduler_rpc_server_config: SchedulerRpcServerConfig = IocManager.config_manager.get(SchedulerRpcServerConfig)
        scheduler_service.initialize(scheduler_rpc_server_config=scheduler_rpc_server_config)

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
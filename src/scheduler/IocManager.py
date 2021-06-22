import os
import sys
from multiprocessing.process import current_process

from injector import singleton, Injector, threadlocal, Binder
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

from infrastructor.dependency.scopes import ISingleton, IScoped
from infrastructor.utils.ConfigManager import ConfigManager
from infrastructor.utils.Utils import Utils
from models.configs.ApplicationConfig import ApplicationConfig
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
        # Configuration initialize
        IocManager.config_manager = ConfigManager(root_directory)
        sys.path.append(root_directory)
        folders = Utils.find_sub_folders(root_directory)
        module_list, module_attr_list = Utils.get_modules(folders)
        IocManager.injector = Injector(IocManager.configure)

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
    def process_info():
        application_config: ApplicationConfig = IocManager.config_manager.get(ApplicationConfig)
        print(f"Application : {application_config.name}")
        print(f"Process Name : {current_process().name}")
        print(f"Pid : {os.getpid()}")
        print(f"Parent Pid : {os.getppid()}")

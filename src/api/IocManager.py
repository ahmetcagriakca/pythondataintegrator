import os
import sys
from flask import Flask
from flask_injector import request, FlaskInjector
from flask_restplus import Api
from injector import singleton, Injector, threadlocal, Binder
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.dependency.scopes import ISingleton, IScoped
from infrastructor.utils.ConfigManager import ConfigManager
from infrastructor.utils.Utils import Utils
from models.configs.ApiConfig import ApiConfig
from models.configs.ApplicationConfig import ApplicationConfig


class IocManager:
    app: Flask = None
    api: Api = None
    binder: Binder = None
    app_wrapper = None
    job_scheduler = None
    scheduler_service = None
    config_manager = None
    injector: Injector = None
    job_event_handler = None
    Base = declarative_base(metadata=MetaData(schema='Common'))

    @staticmethod
    def initialize():
        root_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))
        IocManager.configure_startup(root_directory)

    @staticmethod
    def set_app_wrapper(app_wrapper=None):
        IocManager.app_wrapper = app_wrapper

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
        application_config: ApplicationConfig = IocManager.config_manager.get(ApplicationConfig)
        api_config = IocManager.config_manager.get(ApiConfig)
        if application_config.api_node:
            # ApiConfig getting with type
            IocManager.app = Flask(api_config.name)
            authorizations = {
                'apikey': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'X-API'
                },
                'oauth2': {
                    'type': 'oauth2',
                    'flow': 'accessCode',
                    'tokenUrl': 'https://somewhere.com/token',
                    'authorizationUrl': 'https://somewhere.com/auth',
                    'scopes': {
                        'read': 'Grant read-only access',
                        'write': 'Grant read-write access',
                    }
                }
            }
            IocManager.api = Api(IocManager.app, security=['apikey', {'oauth2': 'read'}], authorizations=authorizations)
            # Flask instantiate
            # IocManager.api = Api(app=IocManager.app,authorizations=authorizations, security='apikey')

            # Importing all modules for dependency
            sys.path.append(api_config.root_directory)
            folders = Utils.find_sub_folders(api_config.root_directory)
            module_list, module_attr_list = Utils.get_modules(folders)
            IocManager.injector = Injector()
            # Flask injector configuration
            FlaskInjector(app=IocManager.app, modules=[IocManager.configure], injector=IocManager.injector)
        elif application_config.process_node:
            sys.path.append(api_config.root_directory)
            folders = Utils.find_sub_folders(api_config.root_directory)
            module_list, module_attr_list = Utils.get_modules(folders)
            IocManager.injector = Injector(IocManager.configure)

    @staticmethod
    def run():
        application_config: ApplicationConfig = IocManager.config_manager.get(ApplicationConfig)
        if application_config.process_node:
            job_scheduler=IocManager.injector.get(IocManager.job_scheduler)
            job_scheduler.run()
            # scheduler_service = SchedulerService()
            IocManager.scheduler_service.initialize(job_scheduler=job_scheduler)

        if application_config.api_node:
            IocManager.injector.get(IocManager.app_wrapper).run()

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

        for controller in ResourceBase.__subclasses__():
            binder.bind(
                controller,
                to=controller,
                scope=request,
            )
        application_config: ApplicationConfig = IocManager.config_manager.get(ApplicationConfig)
        if application_config.api_node:
            if IocManager.app_wrapper is not None:
                api_config = IocManager.config_manager.get(ApiConfig)
                binder.bind(
                    IocManager.app_wrapper,
                    to=IocManager.app_wrapper(api_config)
                )

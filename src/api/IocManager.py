from multiprocessing.process import current_process
import os
import sys
from flask import Flask,redirect
from flask_injector import request, FlaskInjector
from flask_restx import Api
from injector import singleton, Injector, threadlocal, Binder
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from infrastructure.api.ResourceBase import ResourceBase
from infrastructure.dependency.scopes import ISingleton, IScoped
from infrastructure.logging.ConsoleLogger import ConsoleLogger
from infrastructure.utils.ConfigManager import ConfigManager
from infrastructure.utils.Utils import Utils
from models.configs.ApiConfig import ApiConfig
from models.configs.ApplicationConfig import ApplicationConfig
from models.configs.DatabaseConfig import DatabaseConfig
from models.configs.ProcessRpcClientConfig import ProcessRpcClientConfig
from models.configs.SchedulerRpcClientConfig import SchedulerRpcClientConfig



class IocManager:
    app: Flask = None
    api: Api = None
    binder: Binder = None
    app_wrapper = None
    config_manager:ConfigManager = None
    injector: Injector = None
    Base = declarative_base(metadata=MetaData(schema='Common'))

    @staticmethod
    def initialize():
        root_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))
        IocManager.configure_startup(root_directory)

    @staticmethod
    def set_app_wrapper(app_wrapper=None):
        IocManager.app_wrapper = app_wrapper

    @staticmethod
    def initialize_flask():

        application_config: ApplicationConfig = IocManager.config_manager.get(ApplicationConfig)
        api_config: ApiConfig = IocManager.config_manager.get(ApiConfig)
        IocManager.app = Flask(application_config.name)

        @IocManager.app.route('/')
        def home_redirect():
            # Redirect from here, replace your custom site url "www.google.com"
            return redirect("/documentation", code=302, Response=None)
        IocManager.api = Api(IocManager.app,
            title='Python Data Integrator API',
            version='v0.1',
            doc='/documentation',
            base_url='/', security=[api_config.security], authorizations=api_config.authorizations)
        # Flask instantiate
        # IocManager.api = Api(app=IocManager.app,authorizations=authorizations, security='apikey')

    # wrapper required for dependency
    @staticmethod
    def configure_startup(root_directory):
        # Configuration initialize
        IocManager.config_manager = ConfigManager(root_directory)
        IocManager.set_database_application_name()
        IocManager.process_info()

        IocManager.initialize_flask()

        # Importing all modules for dependency
        sys.path.append(root_directory)
        folders = Utils.find_sub_folders(root_directory)
        module_list, module_attr_list = Utils.get_modules(folders)

        IocManager.injector = Injector()
        # Flask injector configuration
        FlaskInjector(app=IocManager.app, modules=[IocManager.configure], injector=IocManager.injector)

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
        if IocManager.app_wrapper is not None:
            api_config = IocManager.config_manager.get(ApiConfig)
            binder.bind(
                IocManager.app_wrapper,
                to=IocManager.app_wrapper(api_config)
            )

    @staticmethod
    def get_process_info():
        return f"{current_process().name} ({os.getpid()},{os.getppid()})"

    @staticmethod
    def process_info():
        logger = ConsoleLogger()
        application_config: ApplicationConfig = IocManager.config_manager.get(ApplicationConfig)
        hostname= f'-{application_config.hostname}' if (application_config.hostname is not None and application_config.hostname!='') else ''
        logger.info(f"Application : {application_config.name}{hostname}")

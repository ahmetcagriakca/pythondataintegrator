import os
from unittest import TestCase

from infrastructor.IocManager import IocManager
from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
from infrastructor.configuration.ConfigService import ConfigService
from infrastructor.delivery.EmailProvider import EmailProvider
from infrastructor.scheduler.JobScheduler import JobScheduler
from models.dao.common.ConfigParameter import ConfigParameter


class TestConfigService(TestCase):
    def __init__(self, methodName='TestConfigService'):
        super(TestConfigService, self).__init__(methodName)

        os.environ["PYTHON_ENVIRONMENT"] = 'test'
        root_directory = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, os.pardir))
        IocManager.configure_startup(root_directory=root_directory,
                                     app_wrapper=FlaskAppWrapper,
                                     job_scheduler=JobScheduler)

    def test_send_email_with_config(self):
        email_provider = IocManager.injector.get(EmailProvider)
        email_provider.send("ahmetcagriakca@gmail.com", "test", "deneme")

    def test_config_service(self):
        config_service = IocManager.injector.get(ConfigService)
        # inserted new config value
        config_parameter = config_service.config_reposiotry.first(Name="NewConfig")
        if config_parameter is not None:
            config_service.database_session_manager.session.delete(config_parameter)
        config_parameter = config_service.config_reposiotry.first(Name="TestNotCached")
        if config_parameter is not None:
            config_service.database_session_manager.session.delete(config_parameter)
        config_parameter = ConfigParameter(Name="NewConfig", Type="str", Value="test", Description="Test config")
        config_service.config_reposiotry.insert(config_parameter)
        config_service.database_session_manager.commit()
        # config value getted from cached method
        value = config_service.get_config_by_name("NewConfig")
        assert value == "test"

        config_parameter = config_service.config_reposiotry.first(Name="NewConfig")
        config_parameter.Value = "testty"
        config_service.database_session_manager.commit()

        # inserted new config value for cache test
        config_parameter = ConfigParameter(Name="TestNotCached", Type="str", Value="test not cached value",
                                           Description="Test config")
        config_service.config_reposiotry.insert(config_parameter)
        value = config_service.get_config_by_name("TestNotCached")
        assert value == "test not cached value"

        # Check  cached value
        value = config_service.get_config_by_name("NewConfig")
        assert value == "test"
        # clear cache
        config_service.get_config_by_name.cache_clear()
        value = config_service.get_config_by_name("TestNotCached")
        assert value == "test not cached value"
        value = config_service.get_config_by_name("NewConfig")
        assert value == "testty"

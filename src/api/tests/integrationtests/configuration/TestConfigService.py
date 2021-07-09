import os
from unittest import TestCase

from IocManager import IocManager
from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
from infrastructor.configuration.ConfigService import ConfigService
from infrastructor.delivery.EmailProvider import EmailProvider
from models.dao.common.ConfigParameter import ConfigParameter


class TestConfigService(TestCase):
    def __init__(self, methodName='TestConfigService'):
        super(TestConfigService, self).__init__(methodName)

        from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
        os.environ["PYTHON_ENVIRONMENT"] = 'test'
        IocManager.set_app_wrapper(app_wrapper=FlaskAppWrapper)
        IocManager.initialize()
        self.client = IocManager.app.test_client()

    def test_send_email_with_config(self):
        email_provider = IocManager.injector.get(EmailProvider)
        email_provider.send("ahmetcagriakca@gmail.com", "test", "deneme")

    def test_config_service(self):
        config_service = IocManager.injector.get(ConfigService)
        # inserted new config value
        config_parameter = config_service.config_reposiotry.first(Name="NewConfig")
        if config_parameter is not None:
            config_service.repository_provider.create().session.delete(config_parameter)
        config_parameter = config_service.config_reposiotry.first(Name="TestNotCached")
        if config_parameter is not None:
            config_service.repository_provider.create().session.delete(config_parameter)
        config_parameter = ConfigParameter(Name="NewConfig", Type="str", Value="test", Description="Test config")
        config_service.config_reposiotry.insert(config_parameter)
        config_service.repository_provider.create().commit()
        # config value getted from cached method
        value = config_service.get_config_by_name("NewConfig")
        assert value == "test"

        config_parameter = config_service.config_reposiotry.first(Name="NewConfig")
        config_parameter.Value = "testty"
        config_service.repository_provider.create().commit()

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

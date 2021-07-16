from IocManager import IocManager
from tests.integrationtests.common.TestApiClient import TestApiClient
from tests.integrationtests.common.TestServiceEndpoints import TestServiceEndpoints
from tests.integrationtests.common.TestServiceScenarios import TestServiceScenarios


class TestManager:
    def __init__(self):
        from infrastructure.api.FlaskAppWrapper import FlaskAppWrapper
        IocManager.set_app_wrapper(app_wrapper=FlaskAppWrapper)
        IocManager.initialize()
        self.client = IocManager.app.test_client()
        self.ioc_manager = IocManager
        self.api_client = TestApiClient(self.client)
        self.service_endpoints = TestServiceEndpoints(self.api_client)
        self.service_scenarios = TestServiceScenarios(service_endpoints=self.service_endpoints,
                                                      ioc_manager=self.ioc_manager)

import os

from infrastructor.IocManager import IocManager
from tests.integrationtests.common.TestApiClient import TestApiClient
from tests.integrationtests.common.TestServiceEndpoints import TestServiceEndpoints
from tests.integrationtests.common.TestServiceScenarios import TestServiceScenarios


class TestManager:
    def __init__(self):
        from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
        from infrastructor.scheduler.JobScheduler import JobScheduler
        os.environ["PYTHON_ENVIRONMENT"] = 'test'
        root_directory = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, os.pardir))
        IocManager.configure_startup(root_directory=root_directory,
                                     app_wrapper=FlaskAppWrapper,
                                     job_scheduler=JobScheduler)
        self.client = IocManager.app.test_client()
        self.ioc_manager = IocManager
        self.api_client = TestApiClient(self.client)
        self.service_endpoints = TestServiceEndpoints(self.api_client)
        self.service_scenarios = TestServiceScenarios(service_endpoints=self.service_endpoints,
                                                      ioc_manager=self.ioc_manager)

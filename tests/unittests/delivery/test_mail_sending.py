import os
from unittest import TestCase
from infrastructor.IocManager import IocManager
from infrastructor.delivery.EmailProvider import EmailProvider


class TestMailSending(TestCase):
    def __init__(self, method_name='TestMailSending'):
        super(TestMailSending, self).__init__(method_name)

        from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
        from infrastructor.scheduler.JobScheduler import JobScheduler
        os.environ["PYTHON_ENVIRONMENT"] = 'test'
        self.root_directory = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, os.pardir))
        IocManager.configure_startup(root_directory=self.root_directory,
                                     app_wrapper=FlaskAppWrapper,
                                     job_scheduler=JobScheduler)
        self.client = IocManager.app.test_client()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def test_get_data_count(self):
        email_provider = IocManager.injector.get(EmailProvider)
        email_provider.send(["ahmetcagriakca@gmail.com"],"test","test")

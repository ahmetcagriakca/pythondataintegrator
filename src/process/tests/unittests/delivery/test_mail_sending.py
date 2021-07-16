import os
from unittest import TestCase
from IocManager import IocManager
from infrastructure.delivery.EmailProvider import EmailProvider


class TestMailSending(TestCase):
    def __init__(self, method_name='TestMailSending'):
        super(TestMailSending, self).__init__(method_name)

        os.environ["PYTHON_ENVIRONMENT"] = 'test'
        IocManager.initialize()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def test_get_data_count(self):
        email_provider = IocManager.injector.get(EmailProvider)
        email_provider.send(["ahmetcagriakca@gmail.com.tr"],"test","test")

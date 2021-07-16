from unittest import TestCase
from IocManager import IocManager
from infrastructure.delivery.EmailProvider import EmailProvider


class TestMailSending(TestCase):
    def __init__(self, method_name='TestMailSending'):
        super(TestMailSending, self).__init__(method_name)

        from infrastructure.api.FlaskAppWrapper import FlaskAppWrapper
        os.environ["PYTHON_ENVIRONMENT"] = 'test'
        IocManager.set_app_wrapper(app_wrapper=FlaskAppWrapper)
        IocManager.initialize()
        self.client = IocManager.app.test_client()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def test_get_data_count(self):
        email_provider = IocManager.injector.get(EmailProvider)
        email_provider.send(["ahmetcagriakca@gmail.com.tr"],"test","test")

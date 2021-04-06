from unittest import TestCase

import os

from infrastructor.IocManager import IocManager


class test_dynamic_call:
    def __init__(self, i):
        self.val = i

    def method_call_test(self, property1, property2=None):
        print(f"val:{self.val}")
        print(f"property1:{property1}")
        print(f"property2:{property2}")
        return property1 + property2


class TestProcess(TestCase):

    def __init__(self, methodName='TestProcess'):
        super(TestProcess, self).__init__(methodName)

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

    @staticmethod
    def static_method_call_test(property1, property2=None):
        print(f"property1:{property1}")
        print(f"property2:{property2}")
        return property1 + property2

    def method_call_test(self, property1, property2=None):
        print(f"property1:{property1}")
        print(f"property2:{property2}")
        return property1 + property2

    def test_dynamic_static_method_call_with_args(self):
        args = (3, 5,)
        method = self.static_method_call_test
        result = method(*args)
        assert result == 8

    def test_dynamic_static_method_call_with_kwargs(self):
        keyword_args = {
            "property2": 5,
            "property1": 3,
        }
        args = [self.static_method_call_test.__name__]
        result = getattr(type(self), args[0])(**keyword_args)
        assert result == 8

    def test_dynamic_method_call_with_kwargs(self):
        keyword_args = {
            "property2": 5,
            "property1": 3,
        }
        args = [test_dynamic_call.method_call_test.__name__]
        # method = getattr(test_dynamic_call, args[0])
        # result = method(test_dynamic_call, **keyword_args)

        instance=test_dynamic_call(i=1)
        result= instance.method_call_test(1,2)
        method = getattr(type(instance), args[0])
        result = method(instance, **keyword_args)
        assert result == 8

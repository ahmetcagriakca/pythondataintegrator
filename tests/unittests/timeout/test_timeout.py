import json
import os
import signal
from unittest import TestCase
from infrastructor.IocManager import IocManager
from infrastructor.connection.queue.QueueProvider import QueueProvider
from models.configs.ApiConfig import ApiConfig
import pandas as pd


class TestTimeout(TestCase):
    def __init__(self, method_name='TestTimeout'):
        super(TestTimeout, self).__init__(method_name)

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
    def loop_forever():
        import time
        while 1:
            print("sec")
            time.sleep(1)

    @staticmethod
    def handler(signum, frame):
        print("Forever is over!")
        raise Exception("end of time")

    def test_timeout(self):
        signal.signal(signal.SIGALRM, TestTimeout.handler)
        signal.alarm(10)
        try:
            TestTimeout.loop_forever()
        except Exception as exc:
            print(exc)
        finally:
            signal.alarm(0)

    def test_consume_data(self):
        queue_provider = IocManager.injector.get(QueueProvider)
        context = queue_provider.get_context()
        data = context.get_data('optiwisdom_automl_topic_test_data', group_id="consumer_group_id2", start=10,
                                limit=100)
        assert len(data) <= 100

    def test_consume_all_data(self):
        queue_provider = IocManager.injector.get(QueueProvider)
        context = queue_provider.get_context()
        data = context.get_data('optiwisdom_automl_topic_test_data', group_id="consumer_group_id2", start=10,
                                limit=100)
        assert len(data) <= 100

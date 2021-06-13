import json
import os
from unittest import TestCase
from infrastructor.IocManager import IocManager
from infrastructor.connection.queue.QueueProvider import QueueProvider
from models.configs.ApiConfig import ApiConfig
import pandas as pd


class TestFileOperation(TestCase):
    def __init__(self, method_name='TestFileOperation'):
        super(TestFileOperation, self).__init__(method_name)

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

    def test_produce_data(self):
        api_config: ApiConfig = IocManager.injector.get(ApiConfig)
        file = os.path.join(api_config.root_directory, 'files', 'test.csv')

        queue_provider = IocManager.injector.get(QueueProvider)
        context = queue_provider.get_context()
        df = pd.read_csv(file, names=None, sep=';', header=0)
        for rec in json.loads(df.to_json(orient='records')):
            print(rec)
        context.write_data('optiwisdom_automl_topic_test_data', messages=df)

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
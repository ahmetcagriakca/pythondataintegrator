# import json
# import os
# from unittest import TestCase
#
# from models.dao.base import Base
# from pdip.connection.queue import QueueProvider
# import pandas as pd
#
# from models.configs.ApplicationConfig import ApplicationConfig
#
#
# class TestFileOperation(TestCase):
#     def __init__(self, method_name='TestFileOperation'):
#         super(TestFileOperation, self).__init__(method_name)
#         IocManager.initialize()
#
#     def print_error_detail(self, data):
#         print(data['message'] if 'message' in data else '')
#         print(data['traceback'] if 'traceback' in data else '')
#         print(data['message'] if 'message' in data else '')
#
#     def test_produce_data(self):
#         application_config: ApplicationConfig = IocManager.injector.get(ApplicationConfig)
#         file = os.path.join(application_config.root_directory, 'files', 'test.csv')
#
#         queue_provider = IocManager.injector.get(QueueProvider)
#         context = queue_provider.get_context()
#         df = pd.read_csv(file, names=None, sep=';', header=0)
#         for rec in json.loads(df.to_json(orient='records')):
#             print(rec)
#         context.write_data('optiwisdom_automl_topic_test_data', messages=df)
#
#     def test_consume_data(self):
#         queue_provider = IocManager.injector.get(QueueProvider)
#         context = queue_provider.get_context()
#         data = context.get_data('optiwisdom_automl_topic_test_data', group_id="consumer_group_id2", start=10,
#                                 limit=100)
#         assert len(data) <= 100
#
#     def test_consume_all_data(self):
#         queue_provider = IocManager.injector.get(QueueProvider)
#         context = queue_provider.get_context()
#         data = context.get_data('optiwisdom_automl_topic_test_data', group_id="consumer_group_id2", start=10,
#                                 limit=100)
#         assert len(data) <= 100
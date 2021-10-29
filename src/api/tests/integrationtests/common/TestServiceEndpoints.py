# from tests.integrationtests.common.TestApiClient import TestApiClient
#
#
# class TestServiceEndpoints:
#     def __init__(self,
#                  api_client: TestApiClient):
#         self.api_client: TestApiClient = api_client
#
#     def get_connection(self):
#         response_data = self.api_client.get('/api/Connection')
#         return response_data
#
#     def delete_connection(self, request):
#         response_data = self.api_client.delete('/api/Connection', request)
#         return response_data
#
#     def create_connection_database(self, request):
#         response_data = self.api_client.post('/api/Connection/ConnectionDatabase', request)
#         return response_data
#
#     def create_connection_file(self, request):
#         response_data = self.api_client.post('/api/Connection/ConnectionFile', request)
#         return response_data
#
#     def create_connection_queue(self, request):
#         response_data = self.api_client.post('/api/Connection/ConnectionQueue', request)
#         return response_data
#
#     def delete_connection(self, request):
#         response_data = self.api_client.delete('/api/Connection', request)
#         return response_data
#
#     def get_connection_type(self):
#         response_data = self.api_client.get('/api/Connection/ConnectionType')
#         return response_data
#
#     def get_connector_type(self):
#         response_data = self.api_client.get('/api/Connection/ConnectorType')
#         return response_data
#
#     def get_data_integration(self):
#         response_data = self.api_client.get('/api/DataIntegration')
#         return response_data
#
#     def insert_data_integration(self, request):
#         response_data = self.api_client.post('/api/DataIntegration', request)
#         return response_data
#
#     def update_data_integration(self, request):
#         response_data = self.api_client.put('/api/DataIntegration', request)
#         return response_data
#
#     def delete_data_integration(self, request):
#         response_data = self.api_client.delete('/api/DataIntegration', request)
#         return response_data
#
#     def test_get_data_operation(self):
#         response_data = self.api_client.get('/api/DataOperation')
#         return response_data
#
#     def insert_data_operation(self, request):
#         response_data = self.api_client.post('/api/DataOperation', request)
#         return response_data
#
#     def update_data_operation(self, request):
#         response_data = self.api_client.put('/api/DataOperation', request)
#         return response_data
#
#     def delete_data_operation(self, request):
#         response_data = self.api_client.delete('/api/DataOperation', request)
#         return response_data
#
#     def run_schedule_job_operation(self, request):
#         response_data = self.api_client.post('/api/JobScheduler/ScheduleJob', request)
#         return response_data

# from unittest import TestCase
#
# from pdip.data.repository import RepositoryProvider
#
# from pdi.domain.connection.Connection import Connection
# from pdi.domain.connection.ConnectionDatabase import ConnectionDatabase
# from tests.integrationtests.common.TestManager import TestManager
#
#
# class TestConnectionResource(TestCase):
#     def __init__(self, methodName='TestConnectionResource'):
#         super(TestConnectionResource, self).__init__(methodName)
#         self.test_manager = TestManager()
#
#     def test_get_connection(self):
#         response_data = self.test_manager.service_endpoints.get_connection()
#         assert response_data['IsSuccess'] == True
#
#     def test_delete_connection(self):
#         id = 1
#         test_data = {"Id": id}
#         try:
#             response_data = self.test_manager.service_endpoints.delete_connection(test_data)
#             assert response_data["Message"] == "Connection Removed Successfully"
#         except Exception as ex:
#             assert True == False
#         finally:
#             # clean data_integration test operations
#             repository_provider = self.test_manager.ioc_manager.injector.get(RepositoryProvider)
#             connection_database_repository = repository_provider.get(ConnectionDatabase)
#             connection_repository = repository_provider.get(Connection)
#             connection = connection_repository.first(Id=id)
#             connection_database = connection_database_repository.first(Connection=connection)
#             connection.IsDeleted = 0
#             connection_database.IsDeleted = 0
#             repository_provider.commit()

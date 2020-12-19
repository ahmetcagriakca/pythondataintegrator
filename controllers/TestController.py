from flask import jsonify, request
from flask_restplus import fields
from flask_restplus.reqparse import RequestParser
from injector import inject

from controllers.models.CommonModels import CommonModels
from controllers.models.TestModels import TestModels
from domain.pdi.services.TestParallelService import TestParallelService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.data.ConnectionManager import ConnectionManager
from infrastructor.data.ConnectionPolicy import ConnectionPolicy
from infrastructor.logging.SqlLogger import SqlLogger
from models.configs.DatabaseConfig import DatabaseConfig


@TestModels.ns.route('/path/<int:value>/<int:value_for_sum>', doc=False)
class TestResource(ResourceBase):
    @inject
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @TestModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self, value, value_for_sum):
        result = {'sum': value + value_for_sum}
        return CommonModels.get_response(result=result)


@TestModels.ns.route('/query')
class TestResource(ResourceBase):
    @inject
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @TestModels.ns.expect(TestModels.parser, validate=True)
    @TestModels.ns.marshal_with(CommonModels.SuccessModel)
    def get(self):
        data = TestModels.parser.parse_args(request)
        value = data.get('value')  #
        value_for_sum = data.get('value_for_sum')  # This is FileStorage instance
        # url = do_something_with_file(uploaded_file)
        result = {'sum': value + value_for_sum}
        return CommonModels.get_response(result=result)

    @TestModels.ns.expect(TestModels.sum_model, validate=True)
    @TestModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        data = IocManager.api.payload
        value = data.get('value')  #
        value_for_sum = data.get('value_for_sum')  # This is FileStorage instance
        result = {'sum': value + value_for_sum, "test": [{"test": 1}, {"test": 2}]}
        return CommonModels.get_response(result=result)


@TestModels.ns.route('/TestMssqlConnection')
class TestMssqlConnectionResource(ResourceBase):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sql_logger = sql_logger

    @TestModels.ns.expect(TestModels.mssql_model)
    @TestModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        request_json = IocManager.api.payload
        # request_data = json.dumps(request_json)
        # consoleLogger = ConsoleLogger()
        # consoleLogger.info_Log('Test Connection is began with data:' + request_data)
        host = '10.210.118.216\INST05'
        database = 'ONENT'
        user = 'ONENT_PYTH'
        password = 'Pyth123'
        if request_json is not None and len(request_json) > 0:
            host = request_json.get("HOST", host)
            database = request_json.get("DATABASE", database)
            user = request_json.get("USER", user)
            password = request_json.get("PASSWORD", password)
        config = DatabaseConfig(type="MSSQL", host=host, database=database, username=user, password=password)
        database_policy = ConnectionPolicy(config)
        database_manager: ConnectionManager = ConnectionManager(database_policy, self.sql_logger)
        query = 'select * from test_pdi'
        datas = database_manager.fetch(query)
        return CommonModels.get_response(result=datas)


@TestModels.ns.route('/TestOracleConnection')
class TestOracleConnectionResource(ResourceBase):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sql_logger = sql_logger

    @TestModels.ns.expect(TestModels.oracle_model)
    @TestModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        request_json = request.get_json()
        host = '10.201.83.85'
        port = 1521
        database = 'ANKADEV'
        user = 'MAPINFO'
        password = 'd_MAPINFO'
        if request_json is not None and len(request_json) > 0:
            host = request_json.get("HOST", host)
            port = request_json.get("PORT", port)
            database = request_json.get("DATABASE", database)
            user = request_json.get("USER", user)
            password = request_json.get("PASSWORD", password)

        config = DatabaseConfig(type="ORACLE", host=host, port=port, database=database, username=user,
                                password=password)
        database_policy = ConnectionPolicy(config)
        database_manager: ConnectionManager = ConnectionManager(database_policy, self.sql_logger)
        query = 'select * from test_pdi'
        datas = database_manager.fetch(query)

        return CommonModels.get_response(result=datas)

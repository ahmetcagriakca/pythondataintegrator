import json
from unittest import TestCase
import cx_Oracle
import pyodbc
import os
from infrastructor.IocManager import IocManager
from infrastructor.data.ConnectionManager import ConnectionManager
from infrastructor.data.connectors.MssqlDbConnector import MssqlDbConnector
from infrastructor.data.connectors.OracleDbConnector import OracleDbConnector


class PdiControllerTests(TestCase):

    def __init__(self, methodName='runPdiTest'):
        super(PdiControllerTests, self).__init__(methodName)

        from infrastructor.api.FlaskAppWrapper import FlaskAppWrapper
        from infrastructor.scheduler.JobScheduler import JobScheduler

        os.environ["PYTHON_ENVIRONMENT"] = 'test'
        root_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
        IocManager.configure_startup(root_directory=root_directory, 
                                     app_wrapper=FlaskAppWrapper,
                                     job_scheduler=JobScheduler)

        self.client = IocManager.app.test_client()

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def test_oracle_connector(self):
        oracleConnector = OracleDbConnector(None, '10.201.83.85', 1521, 'ANKADEV', 'MAPINFO', 'd_MAPINFO')
        databaseManager = ConnectionManager(oracleConnector)
        datas = databaseManager.fetch('select * from test_pdi');
        assert len(datas) > 0

    def test_mssql_connector(self):
        mssqlConnector = MssqlDbConnector('10.210.118.216\INST05', 'ONENT',
                                          'ONENT_PYTH', 'Pyth123')
        databaseManager = ConnectionManager(mssqlConnector)
        datas = databaseManager.fetch('select * from test_pdi');
        assert len(datas) > 0

    def test_oracle_connection(self):

        # ip = 'lebedev.turkcell.tgc'
        # port = 1521
        # ServiceName = 'ANKA12C'
        # MAPINFO connection details
        ip = '10.201.83.85'
        port = 1521
        ServiceName = 'ANKADEV'
        prod_tns = cx_Oracle.makedsn(ip, port, service_name=ServiceName)

        username = 'MAPINFO'
        password = 'd_MAPINFO'

        prod_connection = cx_Oracle.connect(username, password, prod_tns)
        query = """ 
        SELECT * FROM test_pdi
        """
        cur = prod_connection.cursor()
        result = cur.execute(query)
        result.to_csv('test_pdi.csv')

    def test_mssql_connection(self):
        try:
            drivers = [item for item in pyodbc.drivers()]
            for drivery in drivers:
                print("driver:{}".format(drivery))
            # local
            driver = 'ODBC Driver 17 for SQL Server'
            server = 'TT17267556.turkcell.entp.tgc'  # 'db'
            db = 'TestDB'
            user = 'SA'
            password = 'Test123456'

            # server
            driver = 'ODBC Driver 17 for SQL Server'
            server = '10.210.118.216\INST05'
            db = 'ONENT'
            user = 'ONENT_PYTH'
            password = 'Pyth123'

            connection_string = 'DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (driver, server, db, user, password)
            sqlConn = pyodbc.connect(connection_string)
            # sqlConn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=VOLVOFCI05.ng.entp.tgc\INST05;Database=ONENT;Trusted_Connection=yes;')
            sqlCursor = sqlConn.cursor()
            sqlCursor.execute('SELECT * FROM NEMS_INTEGRATION.PYTHON_DATA_INTEGRATOR WHERE IS_DELETED=0')
            data = sqlCursor.fetchall()
            x = data
        except pyodbc.Error as ex:
            print(ex)

    def test_post_api_full(self):
        data = json.dumps({
            "Code": "CAGRITEST"
        })

        response = self.client.post(
            '/api/pdi/StartOperation',
            data=data,
            content_type='application/json',
        )

        response_data = json.loads(response.get_data(as_text=True))
        print(response_data)
        assert response.status_code == 200
        self.print_error_detail(response_data)
        assert response_data['isSuccess'] == 'true'

    def test_post_api(self):
        data = json.dumps(
            {
                'CODE': 'ZONEINFO'
            }
        )

        response = self.client.post(
            '/api/pdi/start_operation',
            data=data,
            content_type='application/json',
        )

        response_data = json.loads(response.get_data(as_text=True))
        print(response_data)
        assert response.status_code == 200
        self.print_error_detail(response_data)
        assert response_data['isSuccess'] == 'true'

    def test_mssql_connection_service(self):

        data = json.dumps(
            {

            }
        )

        response = self.client.post(
            '/api/pdi/test_mssql_connection',
            data=data,
            content_type='application/json',
        )

        response_data = json.loads(response.get_data(as_text=True))
        print(response_data)
        assert response.status_code == 200
        self.print_error_detail(response_data)
        assert response_data['isSuccess'] == 'true'
        assert len(response_data['result']) > 0

    def test_oracle_connection_service(self):

        data = json.dumps(
            {

            }
        )

        response = self.client.post(
            '/api/pdi/test_oracle_connection',
            data=data,
            content_type='application/json',
        )

        response_data = json.loads(response.get_data(as_text=True))
        print(response_data)
        assert response.status_code == 200
        self.print_error_detail(response_data)
        assert response_data['isSuccess'] == 'true'
        assert len(response_data['result']) > 0

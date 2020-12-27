class ConnectionTestData:
    test_insert_input = {
        "Name": "TestConnection",
        "ConnectionTypeName": "Database",
        "ConnectorTypeName": "POSTGRESQL",
        "Host": "string",
        "Port": 0,
        "Sid": "string",
        "DatabaseName": "string",
        "User": "string",
        "Password": "string"
    }
    test_update_input = {
        "Name": "TestConnection",
        "ConnectorTypeName": "MSSQL",
        "Host": "Test",
        "Port": 1550,
        "Sid": "test",
        "DatabaseName": "test",
        "User": "test",
        "Password": "test"
    }

    test_integration_connection = {
        "Name": "TestIntegrationConnection",
        "ConnectionTypeName": "Database",
        "ConnectorTypeName": "POSTGRESQL",
        "Host": "localhost",
        "Port": 5432,
        "Sid": "",
        "DatabaseName": "test_pdi",
        "User": "postgres",
        "Password": "123456"
    }
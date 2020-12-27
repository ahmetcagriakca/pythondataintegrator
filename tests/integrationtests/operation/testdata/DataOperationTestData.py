class DataOperationTestData:
    test_insert_input = {
        "Name": "TEST_DATA_OPERATION",
        "Integrations": [
            {
                "Code": "TEST_DATA_OPERATION_INTEGRATION",
                "Order": 1,
                "Limit": 10000,
                "ProcessCount": 1
            }
        ]
    }

    test_update_input = {
        "Name": "TEST_DATA_OPERATION",
        "Integrations": [
            {
                "Code": "TEST_DATA_OPERATION_INTEGRATION",
                "Order": 1,
                "Limit": 100000,
                "ProcessCount": 2
            }
        ]
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

    test_data_operation_integration_input = {
        "Code": "TEST_DATA_OPERATION_INTEGRATION",
        "SourceConnectionName": "TestIntegrationConnection",
        "SourceSchema": "test",
        "SourceTableName": "test_integration_source",
        "SourceQuery": "",
        "TargetConnectionName": "TestIntegrationConnection",
        "TargetSchema": "test",
        "TargetTableName": "test_integration_source",
        "TargetQuery": "",
        "IsTargetTruncate": True,
        "IsDelta": True,
        "Comments": "Test integration record",
        "SourceColumns": "Id,Name",
        "TargetColumns": "Id,Name",
        "PreExecutions": "",
        "PostExecutions": ""
    }
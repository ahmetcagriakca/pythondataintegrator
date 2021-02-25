class DataOperationTestData:
    test_insert_input = {
        "Name": "TEST_DATA_OPERATION",
        "Contacts": [
            {"Email": "ahmetcagriakca@gmail.com"}
        ],
        "Integrations": [
            {
                "Limit": 10000,
                "ProcessCount": 1,
                "Integration": {
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
                    "Comments": "Test data_integration record",
                    "SourceColumns": "Id,Name,Value",
                    "TargetColumns": "Id,Name,Value",
                    "PreExecutions": "",
                    "PostExecutions": ""
                }
            }
        ]
    }

    test_update_input = {
        "Name": "TEST_DATA_OPERATION",
        "Contacts": [
            {"Email": "t@t.com"}
        ],
        "Integrations": [
            {
                "Limit": 100000,
                "ProcessCount": 2,
                "Integration": {
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
                    "Comments": "Test data_integration record",
                    "SourceColumns": "Id,Name",
                    "TargetColumns": "Id,Name",
                    "PreExecutions": "",
                    "PostExecutions": ""
                }
            }
        ]
    }

    test_integration_connection = {
        "Name": "TestIntegrationConnection",
        "ConnectorTypeName": "POSTGRESQL",
        "Host": "localhost",
        "Port": 5432,
        "Sid": "",
        "DatabaseName": "test_pdi",
        "User": "postgres",
        "Password": "123456"
    }

    test_insert_input_same_integration_1 = {
        "Name": "TEST_DATA_OPERATION_1",
        "Contacts": [
            {"Email": "ahmetcagriakca@gmail.com"}
        ],
        "Integrations": [
            {
                "Limit": 10000,
                "ProcessCount": 1,
                "Integration": {
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
                    "Comments": "Test data_integration record",
                    "SourceColumns": "Id,Name,Value",
                    "TargetColumns": "Id,Name,Value",
                    "PreExecutions": "",
                    "PostExecutions": ""
                }
            }
        ]
    }

    test_insert_input_same_integration_2 = {
        "Name": "TEST_DATA_OPERATION_2",
        "Contacts": [
            {"Email": "ahmetcagriakca@gmail.com"}
        ],
        "Integrations": [
            {
                "Limit": 10000,
                "ProcessCount": 1,
                "Integration": {
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
                    "Comments": "Test data_integration record",
                    "SourceColumns": "Id,Name,Value",
                    "TargetColumns": "Id,Name,Value",
                    "PreExecutions": "",
                    "PostExecutions": ""
                }
            }
        ]
    }

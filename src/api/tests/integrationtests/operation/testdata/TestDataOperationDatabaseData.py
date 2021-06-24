class TestDataOperationDatabaseData:
    test_insert_input = {
        "Name": "TEST_DATA_OPERATION",
        "Contacts": [
            {"Email": "ahmetcagriakca@gmail.com"}
        ],
        "Integrations": [
            {
                "Limit": 5,
                "ProcessCount": 2,
                "Integration": {
                    "Code": "TEST_DATA_OPERATION_INTEGRATION",
                    "SourceConnections": {

                        "ConnectionName": "TestIntegrationConnection",
                        "Database": {
                            "Schema": "test",
                            "TableName": "test_integration_source",
                            "Query": ""
                        },
                        "Columns": "Id,Name,Value",
                    },
                    "TargetConnections": {

                        "ConnectionName": "TestIntegrationConnection",
                        "Database": {
                            "Schema": "test",
                            "TableName": "test_integration_target",
                            "Query": ""
                        },
                        "Columns": "Id,Name,Value",
                    },
                    "IsTargetTruncate": True,
                    "IsDelta": True,
                    "Comments": "Test data_integration record",
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
                "Limit": 5,
                "ProcessCount": 2,
                "Integration": {
                    "Code": "TEST_DATA_OPERATION_INTEGRATION",
                    "SourceConnections": {

                        "ConnectionName": "TestIntegrationConnection",
                        "Database": {
                            "Schema": "test",
                            "TableName": "test_integration_source",
                            "Query": ""
                        },
                        "Columns": "Id,Name,Value",
                    },
                    "TargetConnections": {

                        "ConnectionName": "TestIntegrationConnection",
                        "Database": {
                            "Schema": "test",
                            "TableName": "test_integration_source",
                            "Query": ""
                        },
                        "Columns": "Id,Name,Value",
                    },
                    "IsTargetTruncate": True,
                    "IsDelta": True,
                    "Comments": "Test data_integration record",
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
        "DatabaseName": "test_pdi_integration",
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
                    "SourceConnections": {

                        "ConnectionName": "TestIntegrationConnection",
                        "Database": {
                            "Schema": "test",
                            "TableName": "test_integration_source",
                            "Query": ""
                        },
                        "Columns": "Id,Name,Value",
                    },
                    "TargetConnections": {

                        "ConnectionName": "TestIntegrationConnection",
                        "Database": {
                            "Schema": "test",
                            "TableName": "test_integration_source",
                            "Query": ""
                        },
                        "Columns": "Id,Name,Value",
                    },
                    "IsTargetTruncate": True,
                    "IsDelta": True,
                    "Comments": "Test data_integration record",
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
                    "SourceConnections": {

                        "ConnectionName": "TestIntegrationConnection",
                        "Database": {
                            "Schema": "test",
                            "TableName": "test_integration_source",
                            "Query": ""
                        },
                        "Columns": "Id,Name,Value",
                    },
                    "TargetConnections": {

                        "ConnectionName": "TestIntegrationConnection",
                        "Database": {
                            "Schema": "test",
                            "TableName": "test_integration_source",
                            "Query": ""
                        },
                        "Columns": "Id,Name,Value",
                    },
                    "IsTargetTruncate": True,
                    "IsDelta": True,
                    "Comments": "Test data_integration record",
                }
            }
        ]
    }

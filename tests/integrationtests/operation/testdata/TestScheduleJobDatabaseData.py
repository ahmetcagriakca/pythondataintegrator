class TestScheduleJobData:
    test_job_connection = {
        "Name": "TestIntegrationConnection",
        "ConnectorTypeName": "POSTGRESQL",
        "Host": "localhost",
        "Port": 5432,
        "Sid": "",
        "DatabaseName": "test_pdi_integration",
        "User": "postgres",
        "Password": "123456"
    }

    test_data_operation = {
        "Name": "TEST_JOB_DATA_OPERATION",
        "Contacts": [
            {"Email": "ahmetcagriakca@gmail.com"}
        ],
        "Integrations": [
            {
                "Limit": 100,
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
                        "Columns": "Id,Name",
                    },
                    "TargetConnections": {

                        "ConnectionName": "TestIntegrationConnection",
                        "Database": {
                            "Schema": "test",
                            "TableName": "test_integration_target",
                            "Query": ""
                        },
                        "Columns": "Id,Name",
                    },
                    "IsTargetTruncate": True,
                    "IsDelta": True,
                    "Comments": "Test data_integration record",
                }
            },
            {
                "Limit": 100,
                "ProcessCount": 1,
                "Integration": {
                    "Code": "TEST_DATA_OPERATION_INTEGRATION_FOR_UPDATE",
                    "SourceConnections": {

                        "ConnectionName": "TestIntegrationConnection",
                        "Database": {
                            "Schema": "test",
                            "TableName": "test_integration_source",
                            "Query": "select \"Name\",\"Id\"\nfrom test.test_integration_source"
                        },
                        "Columns": "Name,Id",
                    },
                    "TargetConnections": {

                        "ConnectionName": "TestIntegrationConnection",
                        "Database": {
                            "Schema": "test",
                            "TableName": "test_integration_target",
                            "Query": "update test.test_integration_target set \"Name\" =:Name\nwhere \"Id\"=:Id"
                        },
                        "Columns": "Name,Id",
                    },
                    "IsTargetTruncate": False,
                    "IsDelta": True,
                    "Comments": "Test data_integration record",
                }
            },
            {
                "Limit": 0,
                "ProcessCount": 1,
                "Integration": {
                    "Code": "TEST_DATA_OPERATION_INTEGRATION_FOR_QUERY",
                    "TargetConnections": {

                        "ConnectionName": "TestIntegrationConnection",
                        "Database": {
                            "Schema": "test",
                            "TableName": "test_integration_target",
                            "Query": "update test.test_integration_target set \"Name\" =\'query run\'where \"Id\"=1"
                        },
                        "Columns": "",
                    },
                    "IsTargetTruncate": False,
                    "IsDelta": True,
                    "Comments": "Test data_integration record",
                }
            }
        ]
    }

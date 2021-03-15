class ScheduleJobFileTestData:
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
    test_file_connection = {
        "Name": "TestIntegrationConnectionFile",
        "ConnectorTypeName": "CSV",
        "Folder": "",
        "User": "postgres",
        "Password": "123456"
    }

    test_data_operation = {
        "Name": "TEST_JOB_FILE_DATA_OPERATION",
        "Contacts": [
            {"Email": "ahmetcagriakca@gmail.com"}
        ],
        "Integrations": [
            {
                "Limit": 100,
                "ProcessCount": 1,
                "Integration": {
                    "Code": "TEST_FILE_TO_DB_INTEGRATION",
                    "SourceConnections": {

                        "ConnectionName": "TestIntegrationConnectionFile",
                        "File": {
                            "FileName": "test.csv",
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
                    "Code": "TEST_DB_TO_FILE_INTEGRATION",
                    "SourceConnections": {

                        "ConnectionName": "TestIntegrationConnection",
                        "Database": {
                            "Schema": "test",
                            "TableName": "test_integration_target",
                            "Query": ""
                        },
                        "Columns": "Id,Name",
                    },
                    "TargetConnections": {
                        "ConnectionName": "TestIntegrationConnectionFile",
                        "File": {
                            "FileName": "test_new.csv",
                        },
                        "Columns": "Id,Name",
                    },
                    "IsTargetTruncate": True,
                    "IsDelta": True,
                    "Comments": "Test data_integration record",
                }
            }
        ]
    }

class ScheduleJobTestData:

    test_job_connection = {
        "Name": "TestIntegrationConnection",
        "ConnectionTypeName": "Database",
        "ConnectorTypeName": "POSTGRESQL",
        "Host": "localhost",
        "Port": 5432,
        "Sid": "",
        "DatabaseName": "test_pdi_integration",
        "User": "postgres",
        "Password": "123456"
    }

    test_job_integration = {
        "Code": "TEST_DATA_OPERATION_INTEGRATION",
        "SourceConnectionName": "TestIntegrationConnection",
        "SourceSchema": "test",
        "SourceTableName": "test_integration_source",
        "SourceQuery": "",
        "TargetConnectionName": "TestIntegrationConnection",
        "TargetSchema": "test",
        "TargetTableName": "test_integration_target",
        "TargetQuery": "",
        "IsTargetTruncate": True,
        "IsDelta": True,
        "Comments": "Test integration record",
        "SourceColumns": "Id,Name",
        "TargetColumns": "Id,Name",
        "PreExecutions": "",
        "PostExecutions": ""
    }


    test_job_data_operation = {
        "Name": "TEST_JOB_DATA_OPERATION",
        "Integrations": [
            {
                "Code": "TEST_DATA_OPERATION_INTEGRATION",
                "Order": 1,
                "Limit": 100,
                "ProcessCount": 1
            }
        ]
    }

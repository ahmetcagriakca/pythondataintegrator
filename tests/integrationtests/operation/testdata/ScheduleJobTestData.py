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
        "SourceQuery": 'select "Id","Name"\nfrom test.test_integration_source',
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

    test_job_integration_for_update = {
        "Code": "TEST_DATA_OPERATION_INTEGRATION_FOR_UPDATE",
        "SourceConnectionName": "TestIntegrationConnection",
        "SourceSchema": "test",
        "SourceTableName": "test_integration_source",
        "SourceQuery": 'select "Name","Id"\nfrom test.test_integration_source',
        "TargetConnectionName": "TestIntegrationConnection",
        "TargetSchema": "test",
        "TargetTableName": "test_integration_target",
        "TargetQuery": 'update test.test_integration_target set "Name" =:Name\nwhere "Id"=:Id',
        "IsTargetTruncate": False,
        "IsDelta": True,
        "Comments": "Test integration record",
        "SourceColumns": "Name,Id",
        "TargetColumns": "Name,Id",
        "PreExecutions": "",
        "PostExecutions": ""
    }

    test_job_integration_for_target_query = {
        "Code": "TEST_DATA_OPERATION_INTEGRATION_FOR_QUERY",
        "SourceConnectionName": "",
        "SourceSchema": "",
        "SourceTableName": "",
        "SourceQuery": '',
        "TargetConnectionName": "TestIntegrationConnection",
        "TargetSchema": "test",
        "TargetTableName": "test_integration_target",
        "TargetQuery": 'update test.test_integration_target set "Name" =\'query run\'where "Id"=1',
        "IsTargetTruncate": False,
        "IsDelta": True,
        "Comments": "Test integration record",
        "SourceColumns": "Name,Id",
        "TargetColumns": "Name,Id",
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
            },
            {
                "Code": "TEST_DATA_OPERATION_INTEGRATION_FOR_UPDATE",
                "Order": 2,
                "Limit": 100,
                "ProcessCount": 1
            },
            {
                "Code": "TEST_DATA_OPERATION_INTEGRATION_FOR_QUERY",
                "Order": 3,
                "Limit": 0,
                "ProcessCount": 1
            }
        ]
    }

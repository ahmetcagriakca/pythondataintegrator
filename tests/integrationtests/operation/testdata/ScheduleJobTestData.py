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

    test_data_operation = {
        "Name": "TEST_JOB_DATA_OPERATION",
        "Integrations": [
            {
                "Limit": 100,
                "ProcessCount": 1,
                "Integration":{
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
                    "Comments": "Test data_integration record",
                    "SourceColumns": "Id,Name",
                    "TargetColumns": "Id,Name",
                    "PreExecutions": "",
                    "PostExecutions": ""
                }
            },
            {
                "Limit": 100,
                "ProcessCount": 1,
                "Integration":{
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
                    "Comments": "Test data_integration record",
                    "SourceColumns": "Name,Id",
                    "TargetColumns": "Name,Id",
                    "PreExecutions": "",
                    "PostExecutions": ""
                }
            },
            {
                "Limit": 0,
                "ProcessCount": 1,
                "Integration":{
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
                    "Comments": "Test data_integration record",
                    "SourceColumns": "Name,Id",
                    "TargetColumns": "Name,Id",
                    "PreExecutions": "",
                    "PostExecutions": ""
                }
            }
        ]
    }

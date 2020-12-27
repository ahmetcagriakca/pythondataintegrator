class DataIntegrationTestData:
    test_insert_input = {
        "Code": "TEST_INTEGRATION",
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

    test_update_input = {
        "Code": "TEST_INTEGRATION",
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
        "SourceColumns": "Id,Name,Order",
        "TargetColumns": "Id,Name,Order",
        "PreExecutions": "",
        "PostExecutions": ""
    }
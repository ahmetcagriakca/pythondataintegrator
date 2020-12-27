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

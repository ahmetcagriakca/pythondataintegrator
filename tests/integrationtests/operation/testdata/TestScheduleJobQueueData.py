class TestScheduleJobQueueData:
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
    test_queue_connection = {
        "Name": "TestIntegrationConnectionQueue",
        "ConnectorTypeName": "Kafka",
        "Servers": [{
            "Host": "localhost",
            "Port": 29092
        }],
        "Protocol": "",
        "Mechanism": "",
        "User": "",
        "Password": ""
    }
    test_file_connection = {
        "Name": "TestIntegrationConnectionFile",
        "ConnectorTypeName": "CSV",
        "Host": "",
        "Port": 0,
        "User": "",
        "Password": ""
    }

    test_data_operation = {
        "Name": "TEST_JOB_FILE_DATA_OPERATION",
        "Contacts": [
            {"Email": "ahmetcagriakca@gmail.com"}
        ],
        "Integrations": [
            {
                "Limit": 10,
                "ProcessCount": 1,
                "Integration": {
                    "Code": "TEST_CSV_TO_DB_INTEGRATION",
                    "SourceConnections": {

                        "ConnectionName": "TestIntegrationConnectionFile",
                        "File": {
                            "Folder": "",
                            "FileName": "test.csv",
                            "Csv": {
                                "HasHeader": True,
                                "Header": "Id;Name",
                                "Separator": ";",
                            }
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
                "Limit": 10,
                "ProcessCount": 1,
                "Integration": {
                    "Code": "TEST_DB_TO_QUEUE_INTEGRATION",
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
                        "ConnectionName": "TestIntegrationConnectionQueue",
                        "Queue": {
                            "TopicName": "test_pdi_queue_topic",
                        },
                        "Columns": "Id,Name",
                    },
                    "IsTargetTruncate": True,
                    "IsDelta": True,
                    "Comments": "Test data_integration record",
                }
            },

            {
                "Limit": 10,
                "ProcessCount": 1,
                "Integration": {
                    "Code": "TEST_QUEUE_TO_FILE_INTEGRATION",
                    "SourceConnections": {

                        "ConnectionName": "TestIntegrationConnectionQueue",
                        "Queue": {
                            "TopicName": "test_pdi_queue_topic",
                        },
                        "Columns": "Id,Name",
                    },
                    "TargetConnections": {
                        "ConnectionName": "TestIntegrationConnectionFile",
                        "File": {
                            "Folder": "",
                            "FileName": "test_queue.csv",
                            "Csv": {
                                "HasHeader": True,
                                "Header": "a-b",
                                "Separator": "-",
                            }
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

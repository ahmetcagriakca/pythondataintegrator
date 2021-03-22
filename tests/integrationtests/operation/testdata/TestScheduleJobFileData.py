class TestScheduleJobFileData:
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
                "Limit": 100,
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
                                "Header": "Id,Name",
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
                "Limit": 100,
                "ProcessCount": 1,
                "Integration": {
                    "Code": "TEST_DB_TO_CSV_NONE_HEADER_INTEGRATION",
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
                            "Folder": "",
                            "FileName": "test_new_none_header.csv",
                            "Csv": {
                                "HasHeader": False,
                                "Header": "",
                                "Separator": ",",
                            }
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
                    "Code": "TEST_CSV_TO_CSV_INTEGRATION",
                    "SourceConnections": {

                        "ConnectionName": "TestIntegrationConnectionFile",
                        "File": {
                            "Folder": "",
                            "FileName": "test_new_none_header.csv",
                            "Csv": {
                                "HasHeader": False,
                                "Header": "Id,Name",
                                "Separator": ",",
                            }
                        },
                        "Columns": "Name,Id",
                    },
                    "TargetConnections": {
                        "ConnectionName": "TestIntegrationConnectionFile",
                        "File": {
                            "Folder": "",
                            "FileName": "test_new_change_column_order.csv",
                            "Csv": {
                                "HasHeader": True,
                                "Header": "Name;Id",
                                "Separator": ";",
                            }
                        },
                        "Columns": "Name,Id",
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
                    "Code": "TEST_CSV_TO_CSV_INTEGRATION",
                    "SourceConnections": {

                        "ConnectionName": "TestIntegrationConnectionFile",
                        "File": {
                            "Folder": "",
                            "FileName": "test_new_none_header.csv",
                            "Csv": {
                                "HasHeader": False,
                                "Header": "Id,Name",
                                "Separator": ",",
                            }
                        },
                        "Columns": "Id",
                    },
                    "TargetConnections": {
                        "ConnectionName": "TestIntegrationConnectionFile",
                        "File": {
                            "Folder": "",
                            "FileName": "test_new_only_id.csv",
                            "Csv": {
                                "HasHeader": True,
                                "Header": "Id",
                                "Separator": ";",
                            }
                        },
                        "Columns": "Id",
                    },
                    "IsTargetTruncate": True,
                    "IsDelta": True,
                    "Comments": "Test data_integration record",
                }
            },
        ]
    }

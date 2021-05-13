from infrastructor.json.JsonConvert import JsonConvert


@JsonConvert.register
class DataIntegrationConnectionDatabase:
    def __init__(self,
                 Schema: str = None,
                 TableName: str = None,
                 Query: str = None,
                 ):
        self.Schema: str = Schema
        self.TableName: str = TableName
        self.Query: str = Query

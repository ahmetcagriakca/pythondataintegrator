class CreateDataIntegrationModel:
    def __init__(self,
                 Code: str = None,
                 SourceConnectionName: str = None,
                 SourceSchema: str = None,
                 SourceTableName: str = None,
                 SourceQuery: str = None,
                 TargetConnectionName: str = None,
                 TargetSchema: str = None,
                 TargetTableName: str = None,
                 TargetQuery: str = None,
                 IsTargetTruncate: bool = None,
                 IsDelta: bool = None,
                 Comments: str = None,
                 SourceColumns: str = None,
                 TargetColumns: str = None,
                 PreExecutions: str = None,
                 PostExecutions: str = None,
                 ):
        self.Code: str = Code
        self.SourceConnectionName: str = SourceConnectionName
        self.SourceSchema: str = SourceSchema
        self.SourceTableName: str = SourceTableName
        self.SourceQuery: str = SourceQuery
        self.TargetConnectionName: str = TargetConnectionName
        self.TargetSchema: str = TargetSchema
        self.TargetTableName: str = TargetTableName
        self.TargetQuery: str = TargetQuery
        self.IsTargetTruncate: bool = IsTargetTruncate
        self.IsDelta = IsDelta
        self.Comments: str = Comments
        self.SourceColumns: str = SourceColumns
        self.TargetColumns: str = TargetColumns
        self.PreExecutions: str = PreExecutions
        self.PostExecutions: str = PostExecutions

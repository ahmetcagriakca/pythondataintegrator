class UpdateIntegrationDataModel:
    def __init__(self,
                 Code: str = None,
                 SourceConnectionId: int = None,
                 SourceSchema: str = None,
                 SourceTableName: str = None,
                 TargetConnectionId: str = None,
                 TargetSchema: str = None,
                 TargetTableName: str = None,
                 IsTargetTruncate: bool = None,
                 IsDelta: bool = None,
                 Comments: str = None,
                 SourceColumns: str = None,
                 TargetColumns: str = None,
                 PreExecutions: str = None,
                 PostExecutions: str = None,
                 ):
        self.Code: str = Code
        self.SourceConnectionId: int = SourceConnectionId
        self.SourceSchema: str = SourceSchema
        self.SourceTableName: str = SourceTableName
        self.TargetConnectionId: int = TargetConnectionId
        self.TargetSchema: str = TargetSchema
        self.TargetTableName: str = TargetTableName
        self.IsTargetTruncate: bool = IsTargetTruncate
        self.IsDelta = IsDelta
        self.Comments: str = Comments
        self.SourceColumns: str = SourceColumns
        self.TargetColumns: str = TargetColumns
        self.PreExecutions: str = PreExecutions
        self.PostExecutions: str = PostExecutions

from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.dto.LimitModifier import LimitModifier


class ExecuteOperationDto:
    def __init__(self,
                 source_connection: DataIntegrationConnection = None,
                 target_connection: DataIntegrationConnection = None,
                 source_query: str = None,
                 target_query: str = None,
                 column_rows=None,
                 first_row: str = None,
                 limit_modifier: LimitModifier = None
                 ):
        self.source_connection: DataIntegrationConnection = source_connection
        self.target_connection: DataIntegrationConnection = target_connection
        self.source_query: str = source_query
        self.target_query: str = target_query
        self.column_rows = column_rows
        self.first_row: str = first_row
        self.limit_modifier: LimitModifier = limit_modifier

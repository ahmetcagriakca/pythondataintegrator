from datetime import datetime
from typing import List
from infrastructure.cqrs.decorators.dtoclass import dtoclass


@dtoclass
class ConnectionTypeDto:
    Id: int = None
    Name: str = None


@dtoclass
class ConnectorTypeDto:
    Id: int = None
    Name: str = None
    ConnectionTypeId: int = None


@dtoclass
class ConnectionDatabaseDto:
    Id: int = None
    Sid: str = None
    ServiceName: str = None
    DatabaseName: str = None
    ConnectorType: ConnectorTypeDto = None


@dtoclass
class ConnectionDto:
    Id: int = None
    Name: str = None
    Database: ConnectionDatabaseDto = None
    ConnectionType: ConnectionTypeDto = None
    ConnectionTypeId: int = None
    IsDeleted: int = None


@dtoclass
class DataIntegrationConnectionDatabaseDto:
    Id: int = None
    Schema: str = None
    TableName: str = None
    Query: str = None


@dtoclass
class DataIntegrationConnectionDto:
    Id: int = None
    Connection: ConnectionDto = None
    Database: DataIntegrationConnectionDatabaseDto = None


@dtoclass
class DataIntegrationColumnDto:
    Id: int = None
    SourceColumnName: str = None
    TargetColumnName: str = None


@dtoclass
class DataIntegrationDto:
    Id: int = None
    Code: str = None
    SourceConnection: DataIntegrationConnectionDto = None
    TargetConnection: DataIntegrationConnectionDto = None
    Columns: List[DataIntegrationColumnDto] = None
    IsTargetTruncate: bool = None
    IsDelta: bool = None
    Comments: str = None


@dtoclass
class DataOperationIntegrationDto:
    Id: int = None
    Limit: int = None
    ProcessCount: int = None
    Order: int = None
    Integration: DataIntegrationDto = None


@dtoclass
class DataOperationContactDto:
    Id: int = None
    Email: str = None


@dtoclass
class GetDataOperationDto:
    Id: int = None
    Name: str = None
    Contacts: List[DataOperationContactDto] = None
    Integrations: List[DataOperationIntegrationDto] = None
    DefinitionId: int = None
    Version: int = None
    CreationDate: datetime = None
    LastUpdatedDate: datetime = None
    IsDeleted: int = None

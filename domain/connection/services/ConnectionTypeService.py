from typing import List
from injector import inject

from infrastructor.cryptography.CryptoService import CryptoService
from infrastructor.data.ConnectionProvider import ConnectionProvider
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exception.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionFile import ConnectionFile
from models.dao.connection.ConnectorType import ConnectorType
from models.dao.connection.ConnectionType import ConnectionType
from models.enums.ConnectionTypes import ConnectionTypes
from models.viewmodels.connection.CreateConnectionFileModel import CreateConnectionFileModel
from models.viewmodels.connection.UpdateConnectionFileModel import UpdateConnectionFileModel


class ConnectionTypeService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager
                 ):
        self.database_session_manager = database_session_manager
        self.connection_type_repository: Repository[ConnectionType] = Repository[ConnectionType](
            database_session_manager)

    def get(self) -> List[ConnectionType]:
        """
        Get all
        """
        entities = self.connection_type_repository.filter_by(IsDeleted=0).all()
        return entities

    def get_by_name(self, name) -> ConnectionType:
        """
        Get
        """
        entity = self.connection_type_repository.first(IsDeleted=0, Name=name)
        if entity is None:
            raise OperationalException("Connection Type Not Found")
        return entity

from injector import inject

from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from models.dao.secret import SecretType


class SecretTypeService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 ):
        self.database_session_manager = database_session_manager
        self.secret_type_repository: Repository[SecretType] = Repository[SecretType](
            database_session_manager)

    def get_by_name(self, name) -> SecretType:
        """
        Get secret type
        """
        entity = self.secret_type_repository.first(IsDeleted=0, Name=name)
        return entity

from injector import inject

from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from models.dao.secret import AuthenticationType


class AuthenticationTypeService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 ):
        self.database_session_manager = database_session_manager
        self.authentication_type_repository: Repository[AuthenticationType] = Repository[AuthenticationType](
            database_session_manager)

    def get_by_name(self, name) -> AuthenticationType:
        """
        Get secret type
        """
        entity = self.authentication_type_repository.first(IsDeleted=0, Name=name)
        return entity

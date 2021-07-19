from injector import inject

from domain.common.lookup.LookupDto import LookupDto
from domain.common.lookup.LookupResponse import LookupResponse
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from models.dao.operation import DataOperation


class DataOperationLookupService(IScoped):

    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.data_operation_repository = repository_provider.get(DataOperation)

    def get_data_operation_names(self) -> LookupResponse:
        """
        """
        entities = self.data_operation_repository.filter_by(IsDeleted=0).all()
        lookup_datas = [LookupDto(Id=entity.Id, Name=entity.Name) for entity in entities]
        response = LookupResponse(datas=lookup_datas)
        return response


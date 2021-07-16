from typing import List
from injector import inject

from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from models.dao.operation import DataOperation
from models.dao.operation.DataOperationContact import DataOperationContact
from models.viewmodels.operation.CreateDataOperationContactModel import CreateDataOperationContactModel


class DataOperationContactService(IScoped):

    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.data_operation_contact_repository = repository_provider.get(DataOperationContact)

    def insert(self,
               data_operation: DataOperation,
               data_operation_contact_models: List[CreateDataOperationContactModel]):
        """
        Create Data Operation Contact
        """
        if data_operation_contact_models is not None and len(data_operation_contact_models) > 0:
            for data_operation_contact_model in data_operation_contact_models:
                data_operation_contact = DataOperationContact(Email=data_operation_contact_model.Email,
                                                              DataOperation=data_operation)
                self.data_operation_contact_repository.insert(data_operation_contact)

    def update(self,
               data_operation: DataOperation,
               data_operation_contact_models: List[CreateDataOperationContactModel]):
        """
        Update Data Operation
        """
        if data_operation_contact_models is not None and len(data_operation_contact_models) > 0:
            for data_operation_contact_model in data_operation_contact_models:
                data_operation_contact = self.data_operation_contact_repository.first(IsDeleted=0,
                                                                                      DataOperationId=data_operation.Id,
                                                                                      Email=data_operation_contact_model.Email)
                if data_operation_contact is None:
                    data_operation_contact = DataOperationContact(Email=data_operation_contact_model.Email,
                                                                  DataOperation=data_operation)
                    self.data_operation_contact_repository.insert(data_operation_contact)

        check_existing_contacts = self.data_operation_contact_repository.filter_by(IsDeleted=0,
                                                                                   DataOperationId=data_operation.Id).all()
        for existing_contact in check_existing_contacts:
            found = False

            if data_operation_contact_models is not None and len(data_operation_contact_models) > 0:
                for data_operation_contact_model in data_operation_contact_models:
                    if existing_contact.Email == data_operation_contact_model.Email:
                        found = True

            if not found:
                self.data_operation_contact_repository.delete_by_id(existing_contact.Id)

    def delete_by_data_operation_id(self, data_operation_id: int):
        """
        Delete Data operation
        """

        entities = self.data_operation_contact_repository.filter_by(IsDeleted=0, DataOperationId=data_operation_id)
        for entity in entities:
            self.data_operation_contact_repository.delete_by_id(entity.Id)

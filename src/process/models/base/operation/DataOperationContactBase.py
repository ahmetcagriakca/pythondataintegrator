from models.base.EntityBase import EntityBase
from infrastructor.json.BaseConverter import BaseConverter


@BaseConverter.register
class DataOperationContactBase(EntityBase):

    def __init__(self,
                 DataOperationId: int = None,
                 Email: str = None,
                 DataOperation = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationId: int = DataOperationId
        self.Email: int = Email
        self.DataOperation = DataOperation

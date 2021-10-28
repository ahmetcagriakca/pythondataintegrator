from pdip.json import JsonConvert


@JsonConvert.register
class CreateDataOperationContactModel:
    def __init__(self,
                 Email: str = None,
                 *args, **kwargs):
        self.Email: str = Email

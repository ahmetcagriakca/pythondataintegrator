from infrastructor.json.JsonConvert import JsonConvert


@JsonConvert.register
class DataOperationContact:
    def __init__(self,
                 Email: str = None,
                 *args, **kwargs):
        self.Email: str = Email

from typing import List

from domain.common.decorators.requestclass import requestclass


@requestclass
class DeleteConnectionRequest:
    Id: int = None

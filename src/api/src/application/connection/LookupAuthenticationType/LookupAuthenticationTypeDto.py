from pdip.cqrs.decorators import dtoclass


@dtoclass
class LookupAuthenticationTypeDto:
    Id: int = None
    Name: str = None

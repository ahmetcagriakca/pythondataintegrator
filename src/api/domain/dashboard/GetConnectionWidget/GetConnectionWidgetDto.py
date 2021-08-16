from infrastructure.cqrs.decorators.dtoclass import dtoclass


@dtoclass
class GetConnectionWidgetDto:
    WidgetData: any=None

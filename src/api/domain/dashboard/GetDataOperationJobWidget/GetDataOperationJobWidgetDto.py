from infrastructure.cqrs.decorators.dtoclass import dtoclass


@dtoclass
class GetDataOperationJobWidgetDto:
    WidgetData: any=None

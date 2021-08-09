from infrastructure.cqrs.decorators.dtoclass import dtoclass


@dtoclass
class GetDataOperationWidgetDto:
    WidgetData: any=None

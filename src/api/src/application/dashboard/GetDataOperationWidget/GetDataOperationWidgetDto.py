from pdip.cqrs.decorators import dtoclass


@dtoclass
class GetDataOperationWidgetDto:
    WidgetData: any = None

from pdip.cqrs.decorators import dtoclass


@dtoclass
class GetDataOperationJobWidgetDto:
    WidgetData: any = None

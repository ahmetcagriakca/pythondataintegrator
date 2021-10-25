from pdip.cqrs.decorators import dtoclass


@dtoclass
class GetDataOperationJobExecutionWidgetDto:
    WidgetData: any=None

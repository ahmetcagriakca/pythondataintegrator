from infrastructure.cqrs.decorators.dtoclass import dtoclass


@dtoclass
class GetDataOperationJobExecutionWidgetDto:
    WidgetData: any=None

from domain.common.decorators.dtoclass import dtoclass


@dtoclass
class GetDataOperationJobExecutionWidgetDto:
    WidgetData: any=None

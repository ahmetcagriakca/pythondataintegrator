from domain.common.decorators.dtoclass import dtoclass


@dtoclass
class GetDataOperationWidgetDto:
    WidgetData: any=None

from domain.common.decorators.dtoclass import dtoclass


@dtoclass
class GetDataOperationJobWidgetDto:
    WidgetData: any=None

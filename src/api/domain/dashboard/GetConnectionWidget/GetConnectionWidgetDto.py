from domain.common.decorators.dtoclass import dtoclass


@dtoclass
class GetConnectionWidgetDto:
    WidgetData: any=None

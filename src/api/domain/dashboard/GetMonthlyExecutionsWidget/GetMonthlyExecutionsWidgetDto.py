from domain.common.decorators.dtoclass import dtoclass


@dtoclass
class GetMonthlyExecutionsWidgetDto:
    WidgetData: any=None

from infrastructure.cqrs.decorators.dtoclass import dtoclass


@dtoclass
class GetMonthlyExecutionsWidgetDto:
    WidgetData: any=None

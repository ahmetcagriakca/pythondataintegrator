from pdip.cqrs.decorators import dtoclass


@dtoclass
class GetMonthlyExecutionsWidgetDto:
    WidgetData: any=None

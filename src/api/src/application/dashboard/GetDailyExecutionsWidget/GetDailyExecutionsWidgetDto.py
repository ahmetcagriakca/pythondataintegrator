from pdip.cqrs.decorators import dtoclass


@dtoclass
class GetDailyExecutionsWidgetDto:
    WidgetData: any = None

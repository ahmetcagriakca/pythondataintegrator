from pdip.cqrs.decorators import dtoclass


@dtoclass
class GetConnectionWidgetDto:
    WidgetData: any = None

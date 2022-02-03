from pdip.cqrs.decorators import dtoclass


@dtoclass
class GetExecutionStatusesWidgetDto:
    WidgetData: any = None

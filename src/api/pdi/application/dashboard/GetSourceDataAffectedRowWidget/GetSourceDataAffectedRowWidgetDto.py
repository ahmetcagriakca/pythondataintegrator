from pdip.cqrs.decorators import dtoclass


@dtoclass
class GetSourceDataAffectedRowWidgetDto:
    WidgetData: any = None

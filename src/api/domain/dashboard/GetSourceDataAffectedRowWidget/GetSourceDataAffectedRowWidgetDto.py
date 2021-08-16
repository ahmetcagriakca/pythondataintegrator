from infrastructure.cqrs.decorators.dtoclass import dtoclass


@dtoclass
class GetSourceDataAffectedRowWidgetDto:
    WidgetData: any=None

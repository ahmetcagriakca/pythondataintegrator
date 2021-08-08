from domain.common.decorators.dtoclass import dtoclass


@dtoclass
class GetSourceDataAffectedRowWidgetDto:
    WidgetData: any=None

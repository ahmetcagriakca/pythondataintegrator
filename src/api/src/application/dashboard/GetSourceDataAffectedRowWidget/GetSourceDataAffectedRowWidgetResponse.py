from pdip.cqrs.decorators import responseclass

from src.application.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetDto import \
    GetSourceDataAffectedRowWidgetDto


@responseclass
class GetSourceDataAffectedRowWidgetResponse:
    Data: GetSourceDataAffectedRowWidgetDto = None

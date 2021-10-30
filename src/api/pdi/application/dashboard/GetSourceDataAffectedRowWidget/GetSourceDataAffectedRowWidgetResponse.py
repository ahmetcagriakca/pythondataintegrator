from pdip.cqrs.decorators import responseclass

from pdi.application.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetDto import \
    GetSourceDataAffectedRowWidgetDto


@responseclass
class GetSourceDataAffectedRowWidgetResponse:
    Data: GetSourceDataAffectedRowWidgetDto = None

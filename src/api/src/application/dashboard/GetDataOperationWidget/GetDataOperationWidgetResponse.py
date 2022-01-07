from pdip.cqrs.decorators import responseclass

from src.application.dashboard.GetDataOperationWidget.GetDataOperationWidgetDto import GetDataOperationWidgetDto


@responseclass
class GetDataOperationWidgetResponse:
    Data: GetDataOperationWidgetDto = None

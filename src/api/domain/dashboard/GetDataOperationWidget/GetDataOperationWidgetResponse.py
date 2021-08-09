from infrastructure.cqrs.decorators.responseclass import responseclass
from domain.dashboard.GetDataOperationWidget.GetDataOperationWidgetDto import GetDataOperationWidgetDto


@responseclass
class GetDataOperationWidgetResponse:
	Data: GetDataOperationWidgetDto = None

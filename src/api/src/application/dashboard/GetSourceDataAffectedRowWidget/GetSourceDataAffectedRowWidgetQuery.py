from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetRequest import \
    GetSourceDataAffectedRowWidgetRequest
from src.application.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetResponse import \
    GetSourceDataAffectedRowWidgetResponse


@dataclass
class GetSourceDataAffectedRowWidgetQuery(IQuery[GetSourceDataAffectedRowWidgetResponse]):
    request: GetSourceDataAffectedRowWidgetRequest = None

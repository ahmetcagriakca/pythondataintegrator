from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetRequest import \
    GetSourceDataAffectedRowWidgetRequest
from pdi.application.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetResponse import \
    GetSourceDataAffectedRowWidgetResponse


@dataclass
class GetSourceDataAffectedRowWidgetQuery(IQuery[GetSourceDataAffectedRowWidgetResponse]):
    request: GetSourceDataAffectedRowWidgetRequest = None

from datetime import timedelta, datetime
from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Query

from domain.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetDto import \
    GetSourceDataAffectedRowWidgetDto
from models.dao.operation import DataOperationJobExecutionIntegrationEvent
from models.dao.operation.DataOperationJobExecutionIntegration import DataOperationJobExecutionIntegration


class GetSourceDataAffectedRowWidgetMapping:
    widget_data: str = {
        "id": "sourceDataAffectedRowWidget",
        "chartType": "line",
        "datasets": {
            "yesterday": [
                {
                    "label": "Source Data Count",
                    "data": [
                        190, 300, 340, 220, 290, 390, 250, 380, 410, 380, 320, 290
                    ],
                    "fill": "start"
                },
                {
                    "label": "Affected Row Count",
                    "data": [
                        2200, 2900, 3900, 2500, 3800, 3200, 2900, 1900, 3000, 3400, 4100,
                        3800
                    ],
                    "fill": "start"
                }
            ],
            "today": [
                {
                    "label": "Source Data Count",
                    "data": [
                        410, 380, 320, 290, 190, 390, 250, 380, 300, 340, 220, 290
                    ],
                    "fill": "start"
                },
                {
                    "label": "Affected Row Count",
                    "data": [
                        3000, 3400, 4100, 3800, 2200, 3200, 2900, 1900, 2900, 3900, 2500, 3800
                    ],
                    "fill": "start"
                }
            ]
        },
        "labels": [
            "12am",
            "2am",
            "4am",
            "6am",
            "8am",
            "10am",
            "12pm",
            "2pm",
            "4pm",
            "6pm",
            "8pm",
            "10pm"
        ],
        "options": {
            "spanGaps": False,
            "legend": {
                "display": False
            },
            "maintainAspectRatio": False,
            "tooltips": {
                "position": "nearest",
                "mode": "index",
                "intersect": False
            },
            "layout": {
                "padding": {
                    "left": 24,
                    "right": 32
                }
            },
            "elements": {
                "point": {
                    "radius": 4,
                    "borderWidth": 2,
                    "hoverRadius": 4,
                    "hoverBorderWidth": 2
                }
            },
            "scales": {
                "xAxes": [
                    {
                        "gridLines": {
                            "display": False
                        },
                        "ticks": {
                            "fontColor": "rgba(0,0,0,0.54)"
                        }
                    }
                ],
                "yAxes": [
                    {
                        "gridLines": {
                            "tickMarkLength": 16
                        },
                        "ticks": {
                            "stepSize": 1000
                        }
                    }
                ]
            },
            "plugins": {
                "filler": {
                    "propagate": False
                }
            }
        }
    }

    @classmethod
    def to_dto(cls, queries: List[Query]) -> GetSourceDataAffectedRowWidgetDto:
        dto = GetSourceDataAffectedRowWidgetDto()
        widget_data = cls.widget_data
        source_data_query = queries[0]
        affected_row_query = queries[1]
        last_24_hour_source_data_counts = []
        last_24_hour_affected_row_counts = []
        last_24_hour_labels = []
        now = datetime.now()
        for hour_range in range(12):
            start_hour = now - timedelta(hours=hour_range * 2 + 2)
            end_hour = now - timedelta(hours=hour_range * 2)
            hour_text = end_hour.strftime('%H')
            source_data = source_data_query \
                .filter(
                and_(
                    DataOperationJobExecutionIntegration.StartDate > start_hour,
                    DataOperationJobExecutionIntegration.StartDate < end_hour,
                )
            ) \
                .first()
            affected_row = affected_row_query \
                .filter(
                and_(
                    DataOperationJobExecutionIntegrationEvent.EventDate > start_hour,
                    DataOperationJobExecutionIntegrationEvent.EventDate < end_hour
                )
            ) \
                .first()
            last_24_hour_source_data_counts.append(source_data.Count if source_data.Count is not None else 0)
            last_24_hour_affected_row_counts.append(affected_row.Count if source_data.Count is not None else 0)
            last_24_hour_labels.append(hour_text)
        last_48_hour_source_data_counts = [].extend(last_24_hour_source_data_counts)
        last_48_hour_affected_row_counts = [].extend(last_24_hour_affected_row_counts)
        last_48_hour_labels = [].extend(last_24_hour_labels)
        for hour_range in range(12, 24):
            start_hour = now - timedelta(hours=hour_range * 2 + 2)
            end_hour = now - timedelta(hours=hour_range * 2)
            hour_text = end_hour.strftime('%H')
            source_data = source_data_query \
                .filter(
                and_(
                    DataOperationJobExecutionIntegration.StartDate > start_hour,
                    DataOperationJobExecutionIntegration.StartDate < end_hour,
                )
            ) \
                .first()
            affected_row = affected_row_query \
                .filter(
                and_(
                    DataOperationJobExecutionIntegrationEvent.EventDate > start_hour,
                    DataOperationJobExecutionIntegrationEvent.EventDate < end_hour
                )
            ) \
                .first()
            last_48_hour_source_data_counts.append(source_data.Count if source_data.Count is not None else 0)
            last_48_hour_affected_row_counts.append(affected_row.Count if source_data.Count is not None else 0)
            last_48_hour_labels.append(hour_text)

        widget_data['datasets'] = {
            "24h": [
                {
                    "label": "Source Data Count",
                    "data": list(reversed(last_24_hour_source_data_counts)),
                    "fill": "start"
                },
                {
                    "label": "Affected Row Count",
                    "data": list(reversed(last_24_hour_affected_row_counts)),
                    "fill": "start"
                }
            ],
            "48h": [
                {
                    "label": "Source Data Count",
                    "data": list(reversed(last_48_hour_source_data_counts)),
                    "fill": "start"
                },
                {
                    "label": "Affected Row Count",
                    "data": list(reversed(last_48_hour_affected_row_counts)),
                    "fill": "start"
                }
            ]
        }
        widget_data['labels'] = list(reversed(last_24_hour_labels))
        dto.WidgetData = widget_data
        return dto

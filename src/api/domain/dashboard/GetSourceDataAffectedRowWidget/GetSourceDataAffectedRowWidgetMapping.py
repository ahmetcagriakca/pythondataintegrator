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
    def calculate_source_data_count(cls, source_data_query, start_time, end_time):
        source_data = source_data_query \
            .filter(
            and_(
                DataOperationJobExecutionIntegration.StartDate > start_time,
                DataOperationJobExecutionIntegration.StartDate < end_time,
            )
        ) \
            .first()
        return source_data.Count if source_data.Count is not None else 0

    @classmethod
    def calculate_affected_row_count(cls, affected_row_query, start_time, end_time):
        affected_row = affected_row_query \
            .filter(
            and_(
                DataOperationJobExecutionIntegrationEvent.EventDate > start_time,
                DataOperationJobExecutionIntegrationEvent.EventDate < end_time
            )
        ) \
            .first()
        return affected_row.Count if affected_row.Count is not None else 0

    @classmethod
    def get_label(cls, start_time, end_time):
        hour_text = ''
        if start_time.hour == 0:
            hour_text = f"{start_time.strftime('%A')} "
        hour_text += f"{start_time.strftime('%H')}:{start_time.strftime('%M')}-{end_time.strftime('%H')}:{end_time.strftime('%M')}"
        return hour_text

    @classmethod
    def to_dto(cls, queries: (Query, Query)) -> GetSourceDataAffectedRowWidgetDto:
        dto = GetSourceDataAffectedRowWidgetDto()
        widget_data = cls.widget_data
        source_data_query, affected_row_query = queries
        now = datetime.now()
        if now.hour % 2 == 0:
            calculate_start_date = now.replace(minute=0, second=0)
        else:
            calculate_start_date = now.replace(hour=now.hour - 1, minute=0, second=0)

        start_time = calculate_start_date
        end_time = now
        source_data_count = cls.calculate_source_data_count(source_data_query=source_data_query, start_time=start_time,
                                                            end_time=end_time)
        affected_row_count = cls.calculate_affected_row_count(affected_row_query=affected_row_query,
                                                             start_time=start_time, end_time=end_time)
        label = cls.get_label(start_time=start_time, end_time=end_time)
        last_24_hour_source_data_counts = [source_data_count]
        last_24_hour_affected_row_counts = [affected_row_count]
        last_24_hour_labels = [label]
        for hour_range in range(0, 12):
            start_time = calculate_start_date - timedelta(hours=hour_range * 2 + 2)
            end_time = calculate_start_date - timedelta(hours=hour_range * 2)
            source_data_count = cls.calculate_source_data_count(source_data_query=source_data_query,
                                                                start_time=start_time,
                                                                end_time=end_time)
            affected_row_count = cls.calculate_affected_row_count(affected_row_query=affected_row_query,
                                                                 start_time=start_time, end_time=end_time)
            label = cls.get_label(start_time=start_time, end_time=end_time)
            last_24_hour_source_data_counts.append(source_data_count)
            last_24_hour_affected_row_counts.append(affected_row_count)
            last_24_hour_labels.append(label)
        last_48_hour_source_data_counts = []
        last_48_hour_source_data_counts.extend(last_24_hour_source_data_counts)
        last_48_hour_affected_row_counts = []
        last_48_hour_affected_row_counts.extend(last_24_hour_affected_row_counts)
        last_48_hour_labels = []
        last_48_hour_labels.extend(last_24_hour_labels)

        for hour_range in range(12, 24):
            start_time = calculate_start_date - timedelta(hours=hour_range * 2 + 2)
            end_time = calculate_start_date - timedelta(hours=hour_range * 2)
            source_data_count = cls.calculate_source_data_count(source_data_query=source_data_query,
                                                                start_time=start_time,
                                                                end_time=end_time)
            affected_row_count = cls.calculate_affected_row_count(affected_row_query=affected_row_query,
                                                                 start_time=start_time, end_time=end_time)
            label = cls.get_label(start_time=start_time, end_time=end_time)
            last_48_hour_source_data_counts.append(source_data_count)
            last_48_hour_affected_row_counts.append(affected_row_count)
            last_48_hour_labels.append(label)

        widget_data['datasets'] = {
            "48h": {

                "labels": list(reversed(last_48_hour_labels)),
                "data": [
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
            },
            "24h": {
                "labels": list(reversed(last_24_hour_labels)),
                "data": [
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
                ]
            }

        }
        dto.WidgetData = widget_data
        return dto

from datetime import date, timedelta

import yaml
from sqlalchemy import or_
from sqlalchemy.orm import Query
from sqlalchemy.sql.elements import and_

from src.application.dashboard.GetDataOperationJobExecutionWidget.GetDataOperationJobExecutionWidgetDto import \
    GetDataOperationJobExecutionWidgetDto
from src.domain.operation.DataOperationJobExecution import DataOperationJobExecution


class GetDataOperationJobExecutionWidgetMapping:
    widget_data: str = """
    {
      "id": "dataOperationJobExecutionWidget",
      "data": {
        "value": 333,
        "yesterdayDifference": 13
      },
      "chartType": "bar",
      "datasets": [
        {
          "label": "Execution",
          "data": [221, 428, 492, 471, 413, 344, 294]
        }
      ],
      "labels": [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
      ],
      "options": {
        "spanGaps": false,
        "legend": {
          "display": false
        },
        "maintainAspectRatio": false,
        "layout": {
          "padding": {
            "top": 24,
            "left": 16,
            "right": 16,
            "bottom": 16
          }
        },
        "scales": {
          "xAxes": [
            {
              "display": false
            }
          ],
          "yAxes": [
            {
              "display": false,
              "ticks": {
                // min: 100,
                // max: 500
              }
            }
          ]
        }
      }
    }
    """

    @classmethod
    def to_dto(cls, query: Query) -> GetDataOperationJobExecutionWidgetDto:
        dto = GetDataOperationJobExecutionWidgetDto()

        widget_data = yaml.load(cls.widget_data, yaml.FullLoader)
        today_count = query.filter(DataOperationJobExecution.IsDeleted == 0).first()[0]
        widget_data['data']['value'] = today_count
        yesterday_count = query \
            .filter(
            or_(
                and_(DataOperationJobExecution.IsDeleted == 0, DataOperationJobExecution.CreationDate < date.today()),
                and_(DataOperationJobExecution.IsDeleted == 1, DataOperationJobExecution.LastUpdatedDate > date.today())
            )
        ) \
            .first().Count
        if yesterday_count is not None and yesterday_count != 0:
            widget_data['data']['yesterdayDifference'] = (today_count - yesterday_count) / yesterday_count
        else:
            widget_data['data']['yesterdayDifference'] = 0
            yesterday_count = 0
        last_seven_day_counts = []
        last_seven_day_labels = []
        for date_range in range(7):
            day = date.today() - timedelta(days=date_range)
            day_of_week = (day - timedelta(days=date_range + 1)).strftime('%A')
            result = query \
                .filter(
                or_(
                    and_(DataOperationJobExecution.IsDeleted == 0, DataOperationJobExecution.CreationDate < day),
                    and_(DataOperationJobExecution.IsDeleted == 1, DataOperationJobExecution.LastUpdatedDate > day)
                )
            ) \
                .first()[0]
            last_seven_day_counts.append(result)
            last_seven_day_labels.append(day_of_week)

        widget_data['datasets'] = [{"label": "Execution", "data": list(reversed(last_seven_day_counts))}]
        widget_data['labels'] = list(reversed(last_seven_day_labels))
        widget_data['options']['scales']['yAxes'][0]['ticks']['min'] = min(last_seven_day_counts) - 10
        widget_data['options']['scales']['yAxes'][0]['ticks']['max'] = max(last_seven_day_counts) + 10
        dto.WidgetData = widget_data
        return dto

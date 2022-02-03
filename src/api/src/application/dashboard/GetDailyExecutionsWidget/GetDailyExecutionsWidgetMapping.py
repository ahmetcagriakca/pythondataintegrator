from datetime import date, timedelta, datetime

import yaml
from sqlalchemy import or_
from sqlalchemy.orm import Query
from sqlalchemy.sql.elements import and_

from src.application.dashboard.GetDailyExecutionsWidget.GetDailyExecutionsWidgetDto import GetDailyExecutionsWidgetDto
from src.domain.operation.DataOperationJobExecution import DataOperationJobExecution


class GetDailyExecutionsWidgetMapping:
    widget_data: str = """
    {
      "id": "dailyExecutionsWidget",
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
    def to_dto(cls, query: Query) -> GetDailyExecutionsWidgetDto:
        dto = GetDailyExecutionsWidgetDto()

        widget_data = yaml.load(cls.widget_data, yaml.FullLoader)
        now = datetime.now().replace( hour=0, minute=0, second=0)
        day_start = now
        day_end = now - timedelta(days=-1)
        today_count = query \
            .filter(
            or_(
                and_(DataOperationJobExecution.IsDeleted == 0, DataOperationJobExecution.StartDate > day_start,
                     DataOperationJobExecution.StartDate <= day_end),
                and_(DataOperationJobExecution.IsDeleted == 1, DataOperationJobExecution.StartDate > day_start,
                     DataOperationJobExecution.StartDate <= day_end)
            )
        ) \
            .first().Count
        widget_data['data']['value'] = today_count

        widget_data['data']['todayTotalCount'] = 0
        last_seven_day_counts = []
        last_seven_day_labels = []
        for date_range in range(7):
            day_start = now - timedelta(days=date_range)
            day_end = now - timedelta(days=date_range - 1)

            day_of_week = (day_end).strftime('%A')
            result = query \
                .filter(
                or_(
                    and_(DataOperationJobExecution.IsDeleted == 0, DataOperationJobExecution.StartDate > day_start,
                         DataOperationJobExecution.StartDate <= day_end),
                    and_(DataOperationJobExecution.IsDeleted == 1, DataOperationJobExecution.StartDate > day_start,
                         DataOperationJobExecution.StartDate <= day_end)
                )
            ) \
                .first()[0]
            last_seven_day_counts.append(result)
            last_seven_day_labels.append(day_of_week)

        widget_data['datasets'] = [{"label": "Execution", "data": list(reversed(last_seven_day_counts))}]
        widget_data['labels'] = list(reversed(last_seven_day_labels))

        widget_data['options']['scales']['yAxes'][0]['ticks']['min'] = 0
        widget_data['options']['scales']['yAxes'][0]['ticks']['max'] = max(last_seven_day_counts) + (max(last_seven_day_counts) *10/100)
        dto.WidgetData = widget_data
        return dto

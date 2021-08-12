from datetime import timedelta, datetime

import yaml
from sqlalchemy import and_
from sqlalchemy.orm import Query

from domain.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetDto import GetMonthlyExecutionsWidgetDto
from models.dao.operation.DataOperationJobExecution import DataOperationJobExecution


class GetMonthlyExecutionsWidgetMapping:
    widget_data: str = """
    {
      "id": "monthlyExecutionsWidget",
      "chartType": "line",
      "datasets": {
      },
      "options": {
        "spanGaps": false,
        "legend": {
          "display": false
        },
        "maintainAspectRatio": false,
        tooltips: {
            position: 'nearest',
            mode: 'index',
            intersect: false
        },
        "layout": {
          "padding": {
            "top": 32,
            "left": 32,
            "right": 32
          }
        },
        "elements": {
          "point": {
            "radius": 4,
            "borderWidth": 2,
            "hoverRadius": 4,
            "hoverBorderWidth": 2
          },
          "line": {
            "tension": 0
          }
        },
        "scales": {
          "xAxes": [
            {
              "gridLines": {
                "display": false,
                "drawBorder": false,
                "tickMarkLength": 18
              },
              "ticks": {
                "fontColor": "#ffffff"
              }
            }
          ],
          "yAxes": [
            {
              "display": false,
              "ticks": {
              }
            }
          ]
        },
        "plugins": {
          "filler": {
            "propagate": false
          },
          "xLabelsOnTop": {
            "active": true
          }
        }
      }
    }
    """

    @classmethod
    def get_label(cls, start_date):
        month_text = f"{start_date.strftime('%B')}"
        return month_text

    @classmethod
    def to_dto(cls, queries: (Query, Query)) -> GetMonthlyExecutionsWidgetDto:
        dto = GetMonthlyExecutionsWidgetDto()
        widget_data = yaml.load(cls.widget_data, yaml.FullLoader)
        count_query, minimum_maximum_query = queries
        minimum_start_date = minimum_maximum_query.first().MinimumStartDate
        maximum_start_date = minimum_maximum_query.first().MaximumStartDate
        now = datetime.now()
        if minimum_start_date is not None:
            calculate_start_date = minimum_start_date.replace(day=1, hour=0, minute=0, second=0)
        else:
            calculate_start_date = now.replace(day=1, hour=0, minute=0, second=0)
        if maximum_start_date is not None:
            calculate_end_date = maximum_start_date.replace(hour=0, minute=0, second=0)
        else:
            calculate_end_date = now.replace(hour=0, minute=0, second=0)
        datasets = {}
        end_year = calculate_end_date.year
        end_month = calculate_end_date.month
        for year_range in range(now.year - calculate_start_date.year + 1):
            start_year = calculate_start_date.year + year_range
            start_month = calculate_start_date.month if calculate_start_date.year == start_year else 1
            months_execution_counts = []
            months_execution_labels = []
            if start_year < end_year:
                range_length = 13 - start_month
            elif start_year == end_year:
                range_length = end_month-start_month+1
            else:
                range_length = end_month
            if start_year == calculate_start_date.year:
                for initialize_month in range(start_month-1):
                    start_date = calculate_start_date.replace(year=start_year, month=1 + initialize_month).date()
                    months_execution_counts.append(0)
                    months_execution_labels.append(cls.get_label(start_date=start_date))
            for month_range in range(range_length):
                start_date = calculate_start_date.replace(year=start_year, month=start_month + month_range).date()
                if start_date.month == 12:
                    end_date = calculate_start_date.replace(year=start_year + 1, month=1).date()
                else:
                    end_date = calculate_start_date.replace(year=start_year, month=start_month + month_range + 1).date()
                result = count_query \
                    .filter(
                    and_(
                        DataOperationJobExecution.StartDate > start_date,
                        DataOperationJobExecution.StartDate < end_date
                    )
                ) \
                    .first()

                months_execution_counts.append(result.Count)
                label = cls.get_label(start_date=start_date)
                if now.year == start_date.year and now.month == start_date.month:
                    label += ' (Now)'
                months_execution_labels.append(label)
            if end_year == start_year:
                for initialize_month in range(1, 13 - end_month):
                    start_date = calculate_start_date.replace(year=end_year,
                                                              month=end_month+ initialize_month).date()
                    months_execution_counts.append(0)
                    months_execution_labels.append(cls.get_label(start_date=start_date))
            datasets[str(start_year)] = {
                "labels": months_execution_labels,
                "data": [
                    {
                        "label": "Execution",
                        "data": months_execution_counts,
                        "fill": "start"
                    }
                ]
            }
        widget_data['datasets'] = datasets
        dto.WidgetData = widget_data
        return dto

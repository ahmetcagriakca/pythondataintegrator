import yaml

from domain.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetDto import GetMonthlyExecutionsWidgetDto
from models.dao.operation.DataOperationJobExecution import DataOperationJobExecution


class GetMonthlyExecutionsWidgetMapping:
    widget_data: str = """
    {
      "id": "monthlyExecutionsWidget",
      "chartType": "line",
      "datasets": {
        "2015": [
          {
            "label": "Sales",
            "data": [1.9, 3, 3.4, 2.2, 2.9, 3.9, 2.5, 3.8, 4.1, 3.8, 3.2, 2.9],
            "fill": "start"
          }
        ],
        "2016": [
          {
            "label": "Sales",
            "data": [2.2, 2.9, 3.9, 2.5, 3.8, 3.2, 2.9, 1.9, 3, 3.4, 4.1, 3.8],
            "fill": "start"
          }
        ],
        "2017": [
          {
            "label": "Sales",
            "data": [3.9, 2.5, 3.8, 4.1, 1.9, 3, 3.8, 3.2, 2.9, 3.4, 2.2, 2.9],
            "fill": "start"
          }
        ]
      },
      "labels": [
        "JAN",
        "FEB",
        "MAR",
        "APR",
        "MAY",
        "JUN",
        "JUL",
        "AUG",
        "SEP",
        "OCT",
        "NOV",
        "DEC"
      ],
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
                "min": 1.5,
                "max": 5,
                "stepSize": 0.5
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
    def to_dto(cls, entity: DataOperationJobExecution) -> GetMonthlyExecutionsWidgetDto:
        dto = GetMonthlyExecutionsWidgetDto()
        dto.WidgetData = yaml.load(GetMonthlyExecutionsWidgetMapping.widget_data, yaml.FullLoader)
        return dto


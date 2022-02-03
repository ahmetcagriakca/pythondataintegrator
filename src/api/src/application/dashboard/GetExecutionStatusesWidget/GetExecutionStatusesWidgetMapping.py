from datetime import timedelta, datetime

import yaml
from pdip.integrator.domain.enums import StatusTypes
from sqlalchemy import or_
from sqlalchemy.orm import Query
from sqlalchemy.sql.elements import and_

from src.application.dashboard.GetExecutionStatusesWidget.GetExecutionStatusesWidgetDto import \
    GetExecutionStatusesWidgetDto
from src.domain.operation import DataOperationJobExecution


class GetExecutionStatusesWidgetMapping:
    widget_data: str = """
    {
        id: 'executionStatuses',
        labels: ['Finish', 'Error', 'Unfinished'],
        datasets: {
            today: [
                {
                    label: "Today",
                    data: [92.8, 6.1, 1.1],
                    change: [-0.6, 0.7, 0.1],
                    operationErrorRows: [],
                    operationUnfinishedRows: []
                }
            ],
            yesterday: [
                {
                    label: "Yesterday",
                    data: [77.2, 8.4, 14.4],
                    change: [-2.3, 0.3, -0.2],
                    operationErrorRows: [],
                    operationUnfinishedRows: []
                }
            ],
            'last7': [
                {
                    label: "Last 7 Days",
                    data: [88.2, 9.2, 2.6],
                    change: [1.9, -0.4, 0.3],
                    operationErrorRows: [],
                    operationUnfinishedRows: []
                }
            ]
        },
        options: {
            cutoutPercentage: 75,
            spanGaps: false,
            legend: {
                display: false
            },
            maintainAspectRatio: false,
              plugins: {
                labels: {
                  render: 'percentage',
                  fontColor: ['green', 'red', 'white'],
                  precision: 2
                }
              }
        }
    }
    """

    @classmethod
    def to_dto(cls, queries: (Query, Query)) -> GetExecutionStatusesWidgetDto:
        dto = GetExecutionStatusesWidgetDto()

        statuses_query, data_operations_query = queries
        widget_data = yaml.load(cls.widget_data, yaml.FullLoader)
        now = datetime.now().replace(hour=0, minute=0, second=0)
        day_start = now
        day_end = now - timedelta(days=-1)
        widget_data['datasets']['today'][0]['data'] = cls.get_status_data(statuses_query, day_start, day_end)
        widget_data['datasets']['today'][0]['operationErrorRows'], widget_data['datasets']['today'][0][
            'operationUnfinishedRows'] = cls.get_operation_rows(data_operations_query, day_start,
                                                                 day_end)

        yesterday = now - timedelta(days=1)
        day_start = yesterday
        day_end = yesterday - timedelta(days=-1)
        widget_data['datasets']['yesterday'][0]['data'] = cls.get_status_data(statuses_query, day_start, day_end)
        widget_data['datasets']['yesterday'][0]['operationErrorRows'], widget_data['datasets']['yesterday'][0][
            'operationUnfinishedRows'] = cls.get_operation_rows(data_operations_query, day_start,
                                                                 day_end)

        last7 = now - timedelta(days=7)
        day_start = last7
        day_end = last7 - timedelta(days=-8)
        widget_data['datasets']['last7'][0]['data'] = cls.get_status_data(statuses_query, day_start, day_end)
        widget_data['datasets']['last7'][0]['operationErrorRows'], widget_data['datasets']['last7'][0][
            'operationUnfinishedRows'] = cls.get_operation_rows(data_operations_query, day_start,
                                                                 day_end)
        dto.WidgetData = widget_data
        return dto

    @classmethod
    def get_status_data(cls, query, day_start, day_end):
        today_count_query = query \
            .filter(

            or_(
                and_(DataOperationJobExecution.StartDate > day_start, DataOperationJobExecution.StartDate <= day_end)
            )
        )
        today_finish_count = \
            today_count_query.filter(DataOperationJobExecution.StatusId == StatusTypes.Finish.value).first()[0]
        today_error_count = \
            today_count_query.filter(DataOperationJobExecution.StatusId == StatusTypes.Error.value).first()[0]
        today_not_finished_count = today_count_query.filter(
            and_(DataOperationJobExecution.StatusId != StatusTypes.Finish.value,
                 DataOperationJobExecution.StatusId != StatusTypes.Error.value)).first()[0]

        data = [today_finish_count, today_error_count, today_not_finished_count]

        return data

    @classmethod
    def get_operation_rows(cls, query, day_start, day_end):
        operation_data_not_finished = query \
            .filter(
            or_(
                and_(DataOperationJobExecution.StartDate > day_start, DataOperationJobExecution.StartDate <= day_end)
            )
        ) \
            .filter(and_(DataOperationJobExecution.StatusId != StatusTypes.Finish.value,
                         DataOperationJobExecution.StatusId != StatusTypes.Error.value)) \
            .limit(5)

        operation_data_error = query \
            .filter(
            or_(
                and_(DataOperationJobExecution.StartDate > day_start, DataOperationJobExecution.StartDate <= day_end)
            )
        ) \
            .filter(DataOperationJobExecution.StatusId == StatusTypes.Error.value) \
            .limit(5)
        data_not_finished = [dict(rec) for rec in operation_data_not_finished.all()]
        data_error = [dict(rec) for rec in operation_data_error.all()]

        return data_error, data_not_finished

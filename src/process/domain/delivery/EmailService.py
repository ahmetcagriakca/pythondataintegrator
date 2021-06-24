from datetime import datetime
from typing import List

from injector import inject

from infrastructor.configuration.ConfigService import ConfigService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.delivery.EmailProvider import EmailProvider
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from models.configs.ApplicationConfig import ApplicationConfig
from models.dao.common import OperationEvent
from models.dao.common.Log import Log
from models.dao.common.Status import Status
from models.dao.operation import DataOperationJobExecution, DataOperationJob
from models.dao.operation.DataOperationJobExecutionEvent import DataOperationJobExecutionEvent
from models.enums.events import EVENT_EXECUTION_INITIALIZED


class EmailService(IScoped):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 sql_logger: SqlLogger,
                 email_provider: EmailProvider,
                 config_service: ConfigService,
                 application_config: ApplicationConfig

                 ):
        self.application_config: ApplicationConfig = application_config
        self.database_session_manager = database_session_manager
        self.sql_logger: SqlLogger = sql_logger
        self.email_provider = email_provider
        self.config_service = config_service

    @property
    def default_css(self):
        return '''
            .wrapper{
                margin: 0 auto;
                padding: 20px;
                max-width: 1000px;
            }    
            .container600 {
                width: 300px;
                max-width: 100%;
            }
            
            @media all and (max-width: 600px) {
                .container600 {
                    width: 100% !important;
                }
            }
            
            .col49 {
                width: 49%;
            }
            
            .col2 {
                width: 2%;
            }
            
            .col50 {
                width: 50%;
            }
            
            @media all and (max-width: 599px) {
                .fluid {
                    width: 100% !important;
                }
                .reorder {
                    width: 100% !important;
                    margin: 0 auto 10px;
                }
                .ghost-column {
                    display:none;
                    height:0;
                    width:0;
                    overflow:hidden;
                    max-height:0;
                    max-width:0;
                }
            }
            .mail-column{
                text-align: left;
                padding:4px; 
                font-family: Arial,sans-serif; 
                font-size: 12px; 
                line-height:10px;
            }
            .mail-row{
                text-align: left;
                padding:4px; 
                font-family: Arial,sans-serif; 
                font-size: 10px; 
                line-height:10px;
            }
            .mail-row-nowrap{
                white-space: nowrap;
            }
            table {
              border-collapse: collapse;
              width: 100%;
            }
            
            th, td {
              text-align: left;
              padding: 8px;
            }
            
            tr:nth-child(even) {background-color: #f2f2f2;}
            '''

    def mail_html_template(self, body, mail_css=None):
        css = mail_css if mail_css is not None else self.default_css
        template = f'''
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                <title></title>
                <style>{css}</style>
            </head>
            <body>
                {body}
            </body>
        </html>
        '''
        return template

    def get_dict_value(self, dict, key):
        if key in dict:
            return dict[key]
        return ''

    def prepare_table(self, columns: List[str], rows: List[any], width):
        headers = ''
        for column in columns:
            column_style = self.get_dict_value(column, 'style')
            column_class = self.get_dict_value(column, 'class')
            column_value = self.get_dict_value(column, 'value')
            headers = headers + f'<th scope="col" style="{column_style}" class="mail-column {column_class}">{column_value}</th>'
        bodies = ''
        for row in rows:
            bodies = bodies + '<tr>'
            for data in row['data']:
                row_style = self.get_dict_value(data, 'style')
                row_class = self.get_dict_value(data, 'class')
                row_value = self.get_dict_value(data, 'value')
                bodies = bodies + f'<td valign="top" style="{row_style}" class="mail-row {row_class}">{row_value}</td>'
            bodies = bodies + '</tr>'
        table_width = width if width is not None else '100%'

        table = f'''
        <table width="{table_width}" cellpadding="0" cellspacing="0" style="min-width:100%;">
                <thead>
                  {headers}
                </thead>
                <tbody>
                  {bodies}
                </tbody>
            </table>
            '''
        return table

    def add_default_contacts(self, operation_contacts):

        default_contacts = self.config_service.get_config_by_name("DataOperationDefaultContact")
        if default_contacts is not None and default_contacts != '':
            default_contacts_emails = default_contacts.split(",")
            for default_contact in default_contacts_emails:
                if default_contact is not None and default_contact != '':
                    operation_contacts.append(default_contact)

    def send_data_operation_finish_mail(self,
                                        data_operation_job_execution_id,
                                        data_operation_job_execution_status_id,
                                        data_operation_name,
                                        operation_contacts,
                                        execution_table_data,
                                        execution_event_table_data,
                                        execution_integration_table_data
                                        ):
        self.add_default_contacts(operation_contacts=operation_contacts)
        if operation_contacts is None:
            self.sql_logger.info(f'{data_operation_job_execution_id} mail sending contact not found',
                                 job_id=data_operation_job_execution_id)
            return
        subject = f"Execution completed"
        if data_operation_job_execution_status_id == 3:
            subject = subject + " successfully"
        elif data_operation_job_execution_status_id == 4:
            subject = subject + " with error"
        subject = subject + f": {self.application_config.environment} » {data_operation_name} » {data_operation_job_execution_id}"
        execution_table = self.prepare_table(columns=execution_table_data['columns'],
                                             rows=execution_table_data['rows'],
                                             width=800)
        # execution_event_table = self.prepare_table(columns=execution_event_table_data['columns'],
        #                                            rows=execution_event_table_data['rows'],
        #                                            width=400)
        execution_integration_table = self.prepare_table(columns=execution_integration_table_data['columns'],
                                                         rows=execution_integration_table_data['rows'],
                                                         width=None)

        # <div style="font-size: 24px;"><b>Data Operation Events</b></div>
        # {execution_event_table}
        body_content = f'''
                <div class="wrapper">
                    <div style="font-size: 24px;"><b>Data Operation </b></div>
                    {execution_table}
                    <div style="font-size: 24px;"><b>Data Operation Integrations</b></div>
                    {execution_integration_table}
                </div>
                '''
        mail_body = self.mail_html_template(body_content)

        try:
            self.email_provider.send(operation_contacts, subject, mail_body)
        except Exception as ex:
            self.sql_logger.error(f"Error on mail sending. Error:{ex}")

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


class HtmlTemplateService(IScoped):
    @inject
    def __init__(self,
                 application_config: ApplicationConfig

                 ):
        self.application_config: ApplicationConfig = application_config

    @property
    def default_css(self):
        return '''
            .wrapper{
                margin: 0 auto;
                padding: 20px;
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

    def render_table(self, columns: List[str], rows: List[any], width):
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

    def render_html(self,
                    content,
                    ):

        body_content = f'''
                <div class="wrapper">
                    {content}
                </div>
                '''
        mail_body = self.mail_html_template(body_content)
        return mail_body

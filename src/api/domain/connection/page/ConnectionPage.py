from injector import inject

from domain.page.HtmlTemplateService import HtmlTemplateService, Pagination
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.dependency.scopes import IScoped
from models.dao.connection import Connection, ConnectionDatabase


class ConnectionPage(IScoped):

    @inject
    def __init__(self, repository_provider: RepositoryProvider, html_template_service: HtmlTemplateService):
        super().__init__()
        self.repository_provider = repository_provider
        self.html_template_service = html_template_service

    def render_connection(self, pagination):
        headers = [
            {'value': 'Id'},
            {'value': 'Name'},
            {'value': 'Connection Type'},
            {'value': 'Connector Type'},
            {'value': 'Host'},
            {'value': 'Port'},
            {'value': 'Sid'},
            {'value': 'Service Name'},
            {'value': 'Database Name'},
            {'value': 'Creation Date'},
            {'value': 'Last Update Date'}
        ]

        def prepare_row(data):
            connection: Connection = data.Connection
            connection_database: ConnectionDatabase = data.ConnectionDatabase
            last_update_date = None
            if connection_database.LastUpdatedDate is not None:
                last_update_date = connection_database.LastUpdatedDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3]
            row = {
                "data": [
                    {'value': f'<a href="/Connection/{connection.Id}">{connection.Id}</a>'},
                    {'value': connection.Name},
                    {'value': connection.ConnectionType.Name},
                    {'value': connection_database.ConnectorType.Name},
                    {'value': connection.ConnectionServers[0].Host},
                    {'value': connection.ConnectionServers[0].Port},
                    {'value': connection_database.Sid},
                    {'value': connection_database.ServiceName},
                    {'value': connection_database.DatabaseName},
                    {'value': connection_database.CreationDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3],
                     'class': 'row-nowrap'},
                    {'value': last_update_date, 'class': 'row-nowrap'},
                ]
            }
            return row

        query = self.repository_provider.create().session.query(
            ConnectionDatabase, Connection
        ) \
            .filter(ConnectionDatabase.ConnectionId == Connection.Id) \
            .filter(ConnectionDatabase.IsDeleted == 0)
        # job_execution_integrations = job_execution_integrations_query.all()
        pagination.PageUrl='/Connection{}'
        table_data = self.html_template_service.prepare_table_data_dynamic(query=query,
                                                                           headers=headers,
                                                                           prepare_row=prepare_row,
                                                                           sortable='"ConnectionDatabase"."Id" asc',
                                                                           pagination=pagination)

        table = self.html_template_service.render_table(source=table_data)
        return table

    def render(self, pagination: Pagination):

        table_connection = self.render_connection(pagination)
        return self.html_template_service.render_html(content=f'''  <div style="font-size: 24px;"><b>Connections </b></div>{table_connection}''')

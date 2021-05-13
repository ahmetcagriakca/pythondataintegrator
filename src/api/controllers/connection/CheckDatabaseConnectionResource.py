from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.connection.models.ConnectionModels import ConnectionModels
from domain.connection.services.ConnectionService import ConnectionService
from IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase


@ConnectionModels.ns.route("/CheckConnectionDatabase")
class CheckConnectionDatabaseResource(ResourceBase):
    @inject
    def __init__(self, connection_service: ConnectionService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_service = connection_service

    @ConnectionModels.ns.expect(ConnectionModels.check_connection_database_model, validate=True)
    @ConnectionModels.ns.marshal_with(CommonModels.SuccessModel)
    def post(self):
        """
        Check Database Connection
        """
        data = IocManager.api.payload
        name = data.get('Name')  #
        schema = data.get('Schema')  #
        table = data.get('Table')  #
        connection = self.connection_service.get_by_name(name=name)
        database_context = self.connection_service.database_provider.get_context(connection=connection)
        database_context.connector.connect()
        count_of_table = ''
        if schema is not None and schema != '' and table is not None and table != '':
            try:
                count = database_context.get_table_count(f'select * from "{schema}"."{table}"')
                count_of_table = f"Count of table:{count}"
            except Exception as ex:
                count_of_table = f'Count of table getting error {ex}'
        return CommonModels.get_response(result=f"Connection connected successfully. {count_of_table}")

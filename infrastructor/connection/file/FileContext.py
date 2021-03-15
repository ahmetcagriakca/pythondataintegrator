import base64
import io
import os

from injector import inject
from pandas import DataFrame

from infrastructor.connection.file.connectors.FileConnector import FileConnector
from infrastructor.dependency.scopes import IScoped


class FileContext(IScoped):
    @inject
    def __init__(self,
                 connector: FileConnector
                 ):
        self.connector: FileConnector = connector

    def get_data_count(self, file_name):
        count = self.connector.get_data_count(file_name=file_name)
        return count

    def get_data(self, file_name: str, names: [], start: int, limit: int, header: int, separator: str) -> DataFrame:

        data = self.connector.read_data(file_name=file_name, names=names, start=start, limit=limit, header=header,
                                        separator=separator)

        return data

    def write_to_file(self, file_name: str, data: DataFrame, separator: str):
        self.connector.write_data(file_name=file_name, data=data, separator=separator)

    def recreate_file(self, file_name: str, headers: [], separator: str):
        self.connector.recreate_file(file_name=file_name, headers=headers, separator=separator)

    def delete_file(self, file_name: str):
        self.connector.delete_file(file_name=file_name)

    def prepare_insert_row(self, data, column_rows):
        insert_rows = []
        for extracted_data in data:
            row = []
            for column_row in column_rows:
                prepared_data = extracted_data[column_rows.index(column_row)]
                row.append(prepared_data)
            insert_rows.append(tuple(row))
        return insert_rows

    def get_file_path(self, file_name):
        return os.path.join(self.api_config.root_directory, 'files', file_name)

    def check_file(self, file_name, file_order):
        path = os.path.join(self.api_config.root_directory, 'files', file_name)
        if os.path.exists(path):
            if file_order > 0:
                order = os.path.splitext(file_name)[0].split('__')[1]
                new_file_order = file_order + 1

            new_file_name = os.path.splitext(file_name)[0] + f"__{new_file_order}" + os.path.splitext(file_name)[1]
            return self.check_file(new_file_name, new_file_order)
        else:
            return path, file_name

    def write_binary_file_to_server(self, file, file_name):
        path = os.path.join(self.api_config.root_directory, 'files', file_name)
        chunk = 100000
        while True:
            data = file.read(chunk)
            if not data:
                break
            with open(path, 'ab') as ff:
                ff.write(data)
                ff.close()
        return file_name

    def write_file_to_server(self, file):
        path = os.path.join(self.api_config.root_directory, "files", file.filename)
        file.save(path)
        file.close()

    def read_file_from_server_(self, image_name):
        path = os.path.join(self.api_config.root_directory, "files", image_name)
        f = open(path, 'rb')
        bytes = bytearray(f.read())
        base64_string = base64.b64encode(bytes)
        return base64_string

    def read_file_from_server(self, image_name):
        path = os.path.join(self.api_config.root_directory, "files", image_name)
        file = open(path, 'rb')

        byte_io = io.BytesIO()
        byte_io.write(file.read())
        byte_io.seek(0)

        file.close()
        return byte_io

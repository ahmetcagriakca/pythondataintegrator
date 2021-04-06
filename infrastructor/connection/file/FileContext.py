import base64
import io
import os
import re
from asyncio import Queue
from os import listdir
from os.path import isfile, join, isdir
from typing import List

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

    def get_data_count(self, file):
        count = self.connector.get_data_count(file=file)
        return count

    def get_unpredicted_data(self, file: str, names: [], header: int, separator: str, limit: int, process_count: int,
                             data_queue: Queue, result_queue: Queue):
        data = self.connector.get_unpredicted_data(file=file, names=names, header=header, separator=separator,
                                                   limit=limit, process_count=process_count,
                                                   data_queue=data_queue, result_queue=result_queue)
        return data

    def get_data(self, file: str, names: [], start: int, limit: int, header: int, separator: str) -> DataFrame:

        data = self.connector.get_data(file=file, names=names, start=start, limit=limit, header=header,
                                       separator=separator)

        return data

    def write_to_file(self, file: str, data: DataFrame, separator: str):
        self.connector.write_data(file=file, data=data, separator=separator)

    def recreate_file(self, file: str, headers: [], separator: str):
        self.connector.recreate_file(file=file, headers=headers, separator=separator)

    def delete_file(self, file: str):
        self.connector.delete_file(file=file)

    def get_file_path(self, folder_name: str, file_name: str) -> List[str]:
        file_path = os.path.join(self.connector.host, folder_name, file_name)
        return file_path

    # def get_all_files(self, folder_name: str, file_regex: str) -> List[str]:
    #     folder_path = os.path.join(self.connector.host, folder_name)
    #     regex = re.compile(file_regex)
    #     files = []
    #     for root, dirs, files in os.walk(folder_path):
    #         for file in files:
    #             if regex.match(file):
    #                 files.append(os.path.join(root, file))
    #     return files

    def get_files(self, folder, file_regex)-> List[str]:
        regex = re.compile(file_regex)
        only_files = [f for f in listdir(folder) if isfile(join(folder, f) )and regex.match(f)]
        return only_files

    def get_sub_folders(self, folder):
        only_folders = [f for f in listdir(folder) if isdir(join(folder, f))]
        return only_folders

    def get_all_files(self, folder_name: str, file_regex: str) -> List[str]:
        folder_path = os.path.join(self.connector.host, folder_name)

        sub_folders = self.get_sub_folders(folder_path)
        files = self.get_files(folder_path, file_regex)
        file_list = [join(folder_path, file) for file in files]
        for sub_folder in sub_folders:
            sub_folder_path = join(folder_path, sub_folder)
            files = self.get_files(sub_folder_path, file_regex)
            for file in files:
                file_path = join(sub_folder_path, file)
                file_list.append(file_path)
        return file_list

    def prepare_insert_row(self, data, column_rows):
        insert_rows = []
        for extracted_data in data:
            row = []
            for column_row in column_rows:
                prepared_data = extracted_data[column_rows.index(column_row)]
                row.append(prepared_data)
            insert_rows.append(tuple(row))
        return insert_rows


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

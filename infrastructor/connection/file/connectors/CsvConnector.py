import csv
import os
import pandas as pd
from pandas import DataFrame

from infrastructor.connection.file.connectors.FileConnector import FileConnector


class CsvConnector(FileConnector):
    def __init__(self,
                 folder: str):
        self.folder = folder
        self.data_frame = None

    def connect(self):
        # os.path.isdir(self.folder)
        pass

    def disconnect(self):
        pass
        # try:
        #     if self.file is not None:
        #         self.file.close()
        # except Exception:
        #     pass

    def get_data_count(self, file_name: str):
        file_path = os.path.join(self.folder, file_name)
        with open(file_path) as f:
            count = sum(1 for line in f)
        return count

    def read_data(self, file_name: str, names: [], start: int, limit: int, header: int,
                  separator: str) -> DataFrame:
        file_path = os.path.join(self.folder, file_name)
        data = pd.read_csv(file_path, names=names, sep=separator, header=header, skiprows=start, nrows=limit)

        return data

    def write_data(self, file_name: str, data: DataFrame, separator: str):
        file_path = os.path.join(self.folder, file_name)
        data.to_csv(file_path, mode='a', header=0, sep=separator, index=False)

    def recreate_file(self, file_name: str, headers: [], separator: str):
        file_path = os.path.join(self.folder, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=separator)
            writer.writerow(headers)

    def delete_file(self, file_name: str):
        file_path = os.path.join(self.folder, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)

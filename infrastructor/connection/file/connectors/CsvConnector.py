import csv
import os
import pandas as pd
from pandas import DataFrame

from infrastructor.connection.file.connectors.FileConnector import FileConnector


class CsvConnector(FileConnector):
    def __init__(self,
                 host: str):
        self.host = host
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

    def get_data_count(self, file: str):
        file_path = os.path.join(self.host, file)
        with open(file_path, 'rb') as f:
            count = sum(1 for line in f)
        return count

    def get_data_with_chunk(self, file: str, names: [], start: int, limit: int, header: int,
                            separator: str) -> DataFrame:
        count = 0
        for chunk in pd.read_csv(file, names=names, sep=separator, header=header, chunksize=limit, iterator=True,
                                 low_memory=False):
            count += len(chunk)
            if start < count:
                return chunk

    def read_data(self, file: str, names: [], start: int, limit: int, header: int,
                  separator: str) -> DataFrame:
        file_path = os.path.join(self.host, file)
        data = self.get_data_with_chunk(file_path, names=names, start=start, limit=limit, header=header,
                                        separator=separator)

        return data

    def write_data(self, file: str, data: DataFrame, separator: str):
        file_path = os.path.join(self.host, file)
        data.to_csv(file_path, mode='a', header=0, sep=separator, index=False)

    def recreate_file(self, file: str, headers: [], separator: str):
        self.delete_file(file=file)
        file_path = os.path.join(self.host, file)
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=separator)
            writer.writerow(headers)

    def delete_file(self, file: str):
        file_path = os.path.join(self.host, file)
        if os.path.exists(file_path):
            os.remove(file_path)

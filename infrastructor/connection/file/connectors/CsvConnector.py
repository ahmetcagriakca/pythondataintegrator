import csv
import json
import os
from queue import Queue

import pandas as pd
from pandas import DataFrame

from infrastructor.connection.file.connectors.FileConnector import FileConnector
from infrastructor.connection.models.DataQueueTask import DataQueueTask


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

    def start_get_data(self, file: str, names: [], header: int, separator: str, limit: int, data_queue: Queue,
                       result_queue: Queue):
        file_path = os.path.join(self.host, file)
        for chunk in pd.read_csv(file_path, names=names, sep=separator, header=header, chunksize=limit, iterator=True,
                                 low_memory=False):
            data = json.loads(chunk.to_json(orient='records'))
            data_queue_task = DataQueueTask(Data=data, IsFinished=False)
            data_queue.put(data_queue_task)
            result = result_queue.get()
            if result == False:
                break;

    def get_data_count(self, file: str):
        file_path = os.path.join(self.host, file)
        with open(file_path, 'rb') as f:
            count = sum(1 for line in f)
        return count

    def get_data(self, file: str, names: [], start: int, limit: int, header: int,
                 separator: str) -> DataFrame:
        file_path = os.path.join(self.host, file)
        count = 0
        for chunk in pd.read_csv(file_path, names=names, sep=separator, header=header, chunksize=limit, iterator=True,
                                 low_memory=False):
            count += len(chunk)
            if start < count:
                return chunk

        return None

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

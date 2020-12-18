from typing import List

from models.dao.integration.PythonDataIntegrationColumn import PythonDataIntegrationColumn
from models.dto.LimitModifier import LimitModifier


class PdiUtils:
    @staticmethod
    def count_table(schema, table, connector_type):
        if connector_type == 'POSTGRESQL':
            schema = '"' + schema + '"'
            table = '"' + table + '"'
        return f"SELECT COUNT(*)  FROM {schema}.{table}"

    @staticmethod
    def truncate_table(schema, table, connector_type):
        if connector_type == 'POSTGRESQL':
            schema = '"' + schema + '"'
            table = '"' + table + '"'
        return f"DELETE FROM {schema}.{table}"

    @staticmethod
    def insert_into_table(schema, table, row_columns, row_values, connector_type):
        if connector_type == 'POSTGRESQL':
            schema = '"' + schema + '"'
            table = '"' + table + '"'
        return f"INSERT INTO {schema}.{table}({row_columns}) VALUES ({row_values})"

    @staticmethod
    def mssql_executable_script(schema, table, sub_limit, top_limit, selected_rows, first_row):
        return f"WITH TEMP_INTEGRATION AS(SELECT {selected_rows},RowNum = ROW_NUMBER() OVER ( order by {first_row} ) FROM {schema}.{table}) SELECT * FROM TEMP_INTEGRATION WHERE RowNum >= {sub_limit} AND RowNum < {top_limit}"

    @staticmethod
    def oracle_executable_script(schema, table, sub_limit, top_limit, selected_rows, first_row):
        return f"SELECT * FROM (SELECT {selected_rows}, rownum r from {schema}.{table} M) WHERE r >= {sub_limit} and r < {top_limit}"

    @staticmethod
    def postgresql_executable_script(schema, table, sub_limit, top_limit, selected_rows, first_row):
        schema = '"' + schema + '"'
        table = '"' + table + '"'
        first_row = '"' + first_row + '"'
        return f"WITH TEMP_INTEGRATION AS(SELECT {selected_rows},ROW_NUMBER() OVER ( order by {first_row} ) FROM {schema}.{table}) SELECT * FROM TEMP_INTEGRATION WHERE ROW_NUMBER >= {sub_limit} AND ROW_NUMBER < {top_limit}"

    #################################################################
    @staticmethod
    def prepare_insert_row(extracted_datas, related_columns):
        inserted_rows = []
        for extracted_data in extracted_datas:
            inserted_row = []
            for related_column in related_columns:
                inserted_row.append(extracted_data[related_columns.index(related_column)])
            inserted_rows.append(tuple(inserted_row))
        return inserted_rows

    @staticmethod
    def get_limit_modifiers(data_count, limit):
        top_limit = limit+1
        sub_limit = 1
        limit_modifiers = []
        while True:
            if top_limit != limit and top_limit - data_count > limit:
                break
            limit_modifier = LimitModifier(top_limit=top_limit, sub_limit=sub_limit)
            limit_modifiers.append(limit_modifier)
            top_limit += limit
            sub_limit += limit
        return limit_modifiers

    #######################################################################################
    @staticmethod
    def prepare_executable_script(source_connector_type: str, source_schema: str,
                                  source_table_name: str, sub_limit, top_limit, first_row, selected_rows):
        if source_connector_type == 'ORACLE':
            executable_script = PdiUtils.oracle_executable_script(source_schema, source_table_name, sub_limit,
                                                                  top_limit, selected_rows, first_row)
        elif source_connector_type == 'MSSQL':
            executable_script = PdiUtils.mssql_executable_script(source_schema, source_table_name, sub_limit,
                                                                 top_limit, selected_rows, first_row)
        elif source_connector_type == 'POSTGRESQL':
            executable_script = PdiUtils.postgresql_executable_script(source_schema, source_table_name, sub_limit,
                                                                      top_limit, selected_rows, first_row)
        return executable_script

    #######################################################################################
    @staticmethod
    def prepare_executable_scripts(data_count: int, source_connector_type: str, source_schema: str,
                                   source_table_name: str, column_rows, limit: int = 10000):
        top_limit = limit
        sub_limit = 0
        first_row, selected_rows = PdiUtils.get_first_row_and_selected_rows(column_rows)
        paired_executable_list = list()
        if source_connector_type == 'ORACLE':
            while True:
                if top_limit != limit and top_limit - data_count > limit:
                    break
                executable_script = PdiUtils.oracle_executable_script(source_schema, source_table_name, sub_limit,
                                                                      top_limit)
                paired_executable_list.append(executable_script)
                top_limit += limit
                sub_limit += limit
        elif source_connector_type == 'MSSQL':
            while True:
                if top_limit != limit and top_limit - data_count > limit:
                    break
                executable_script = PdiUtils.mssql_executable_script(source_schema, source_table_name, sub_limit,
                                                                     top_limit, selected_rows, first_row)
                paired_executable_list.append(executable_script)
                top_limit += limit
                sub_limit += limit
        elif source_connector_type == 'POSTGRESQL':
            while True:
                if top_limit != limit and top_limit - data_count > limit:
                    break
                executable_script = PdiUtils.postgresql_executable_script(source_schema, source_table_name, sub_limit,
                                                                          top_limit, selected_rows, first_row)
                paired_executable_list.append(executable_script)
                top_limit += limit
                sub_limit += limit
        return paired_executable_list

    @staticmethod
    def get_first_row_and_selected_rows(column_rows):
        selected_rows = ""
        eliminated_column_rows = [column_row for column_row in column_rows if column_row[1] is not None]
        first_row = eliminated_column_rows[0][1]
        for column_rows in eliminated_column_rows:
            selected_rows += f'{"" if column_rows == eliminated_column_rows[0] else ", "}"{column_rows[1].strip()}"'
        return first_row, selected_rows

    @staticmethod
    def get_row_column_and_values(target_connector_type: str, target_schema: str, target_table_name: str,
                                  python_data_integration_columns: List[PythonDataIntegrationColumn]):
        related_columns = []
        column_rows = []
        insert_row_columns = ""
        insert_row_values = ""
        for column in python_data_integration_columns:
            if column.SourceColumnName is not None:
                rel_column = (column.ResourceType, column.SourceColumnName)
                related_columns.append(rel_column)
                row = (column.ResourceType, column.SourceColumnName, column.TargetColumnName)
                column_rows.append(row)
                insert_row_columns += f'{"" if column == python_data_integration_columns[0] else ", "}"{column.TargetColumnName}"'
                if target_connector_type == 'ORACLE':
                    indexer = f':{python_data_integration_columns.index(column)}'
                elif target_connector_type == 'MSSQL':
                    indexer = '?'
                elif target_connector_type == 'POSTGRESQL':
                    indexer = '%s'
                insert_row_values += f'{"" if column == python_data_integration_columns[0] else ", "}{indexer}'
        final_executable = PdiUtils.insert_into_table(target_schema, target_table_name, insert_row_columns,
                                                      insert_row_values, target_connector_type)
        return column_rows, final_executable, related_columns

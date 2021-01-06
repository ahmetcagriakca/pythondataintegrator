from typing import List

from models.dao.integration.DataIntegrationColumn import DataIntegrationColumn
from models.dto.LimitModifier import LimitModifier


class PdiUtils:
    @staticmethod
    def count_table_mssql(query):
        return f"SELECT COUNT(*)  FROM ({query})  as count_table"
    @staticmethod
    def count_table_postgresql(query):
        return f"SELECT COUNT(*)  FROM ({query})  as count_table"
    @staticmethod
    def count_table_oracle(query):
        return f"SELECT COUNT(*)  FROM ({query}) "

    @staticmethod
    def truncate_table(schema, table):
        return f'DELETE FROM "{schema}"."{table}"'

    @staticmethod
    def insert_into_table(schema, table, row_columns, row_values):
        return f'INSERT INTO "{schema}"."{table}"({row_columns}) VALUES ({row_values})'

    @staticmethod
    def mssql_executable_script(query, sub_limit, top_limit, first_row):
        return f"WITH TEMP_INTEGRATION AS(SELECT ordered_query.*, row_number = ROW_NUMBER() OVER ( order by {first_row}) FROM ({query}) as ordered_query) SELECT * FROM TEMP_INTEGRATION WHERE row_number >= {sub_limit} AND row_number < {top_limit}"

    @staticmethod
    def oracle_executable_script(query, sub_limit, top_limit, first_row):
        return f"WITH TEMP_INTEGRATION AS(SELECT ordered_query.*,ROW_NUMBER() OVER ( order by {first_row}) row_number FROM ({query}) ordered_query) SELECT * FROM TEMP_INTEGRATION WHERE row_number >= {sub_limit} and row_number < {top_limit}"

    @staticmethod
    def postgresql_executable_script(query, sub_limit, top_limit, first_row):
        return f"WITH TEMP_INTEGRATION AS(SELECT ordered_query.*,ROW_NUMBER() OVER ( order by {first_row}) row_number FROM ({query}) ordered_query) SELECT * FROM TEMP_INTEGRATION WHERE row_number >= {sub_limit} AND row_number < {top_limit}"

    #################################################################
    @staticmethod
    def prepare_insert_row(extracted_datas, related_columns):
        insert_rows = []
        for extracted_data in extracted_datas:
            inserted_row = []
            for related_column in related_columns:
                inserted_row.append(extracted_data[related_columns.index(related_column)])
            insert_rows.append(tuple(inserted_row))
        return insert_rows

    @staticmethod
    def get_limit_modifiers(data_count, limit):
        top_limit = limit + 1
        sub_limit = 1
        limit_modifiers = []
        id = 0
        while True:
            if top_limit != limit and top_limit - data_count > limit:
                break
            id = id + 1
            limit_modifier = LimitModifier(Id=id, TopLimit=top_limit, SubLimit=sub_limit)
            limit_modifiers.append(limit_modifier)
            top_limit += limit
            sub_limit += limit
        return limit_modifiers

    #######################################################################################
    @staticmethod
    def prepare_executable_script(source_connector_type: str, query: str, sub_limit, top_limit, first_row):
        if source_connector_type == 'ORACLE':
            executable_script = PdiUtils.oracle_executable_script(query=query, sub_limit=sub_limit, top_limit=top_limit,
                                                                  first_row=first_row)
        elif source_connector_type == 'MSSQL':
            executable_script = PdiUtils.mssql_executable_script(query=query, sub_limit=sub_limit, top_limit=top_limit,
                                                                 first_row=first_row)
        elif source_connector_type == 'POSTGRESQL':
            executable_script = PdiUtils.postgresql_executable_script(query=query, sub_limit=sub_limit,
                                                                      top_limit=top_limit, first_row=f'"{first_row}"')
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
    def prepare_target_query(column_rows, query, target_connector_name):
        eliminated_column_rows = [column_row for column_row in column_rows if column_row[1] is not None]
        target_query = query
        for column_rows in eliminated_column_rows:
            if target_connector_name == 'ORACLE':
                indexer = f':{eliminated_column_rows.index(column_rows)}'
            elif target_connector_name == 'MSSQL':
                indexer = '?'
            elif target_connector_name == 'POSTGRESQL':
                indexer = '%s'
            target_query = target_query.replace(f":{column_rows[1]}", indexer)
        return target_query

    @staticmethod
    def get_selected_rows(column_rows):
        selected_rows = ""
        eliminated_column_rows = [column_row for column_row in column_rows if column_row[1] is not None]
        for column_rows in eliminated_column_rows:
            selected_rows += f'{"" if column_rows == eliminated_column_rows[0] else ", "}"{column_rows[1].strip()}"'
        return selected_rows

    @staticmethod
    def get_row_column_and_values(schema: str, table_name: str,
                                  data_integration_columns: List[DataIntegrationColumn]):
        related_columns = []
        column_rows = []
        insert_row_columns = ""
        insert_row_values = ""
        for column in data_integration_columns:
            if column.SourceColumnName is not None:
                rel_column = (column.ResourceType, column.SourceColumnName)
                related_columns.append(rel_column)
                row = (column.ResourceType, column.SourceColumnName, column.TargetColumnName)
                column_rows.append(row)
                insert_row_columns += f'{"" if column == data_integration_columns[0] else ", "}"{column.TargetColumnName}"'
                insert_row_values += f'{"" if column == data_integration_columns[0] else ", "}:{column.SourceColumnName}'
        final_executable = PdiUtils.insert_into_table(schema, table_name, insert_row_columns, insert_row_values)
        return column_rows, related_columns, final_executable

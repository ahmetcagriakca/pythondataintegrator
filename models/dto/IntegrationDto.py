from typing import List
from models.dao.integration.PythonDataIntegration import PythonDataIntegration


class IntegrationDto:
    def __init__(self,
                 python_data_integration: PythonDataIntegration,
                 final_executable: str,
                 executable_script: List[str],
                 related_columns: List[str],
                 unrelated_columns: List[str],
                 ):
        self.python_data_integration: PythonDataIntegration = python_data_integration
        self.final_executable: str = final_executable
        self.executable_scripts: List[str] = executable_script
        self.related_columns: List[str] = related_columns
        self.unrelated_columns: List[str] = unrelated_columns
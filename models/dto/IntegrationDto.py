from typing import List
from models.dao.integration.DataIntegration import DataIntegration


class IntegrationDto:
    def __init__(self,
                 data_integration: DataIntegration,
                 final_executable: str,
                 executable_script: List[str],
                 related_columns: List[str],
                 unrelated_columns: List[str],
                 ):
        self.data_integration: DataIntegration = data_integration
        self.final_executable: str = final_executable
        self.executable_scripts: List[str] = executable_script
        self.related_columns: List[str] = related_columns
        self.unrelated_columns: List[str] = unrelated_columns
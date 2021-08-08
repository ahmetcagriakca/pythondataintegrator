import dataclasses

from generator.domain.DaoGenerateConfig import DaoGenerateConfig


@dataclasses
class GenerateConfig:
    base_directory: str = None
    domain: str = None
    name: str = None
    dao: DaoGenerateConfig = None
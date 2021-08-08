import dataclasses

from generator.domain.GenerateConfig import GenerateConfig


@dataclasses
class QueryGenerateConfig(GenerateConfig):
    is_list = True
    has_paging = False



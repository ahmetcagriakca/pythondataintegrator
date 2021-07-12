from dataclasses import dataclass
from typing import List

from domain.common.lookup.LookupDto import LookupDto


@dataclass
class LookupResponse:
    datas: List[LookupDto] = None

    def to_dict(self):
        return [data.__dict__ for data in self.datas]
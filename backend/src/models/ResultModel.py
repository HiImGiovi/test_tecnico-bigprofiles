from pydantic import BaseModel
from typing import List
from . import EnrichModel
from . import Entry

class ResultModel(BaseModel):
    values: List[EnrichModel]
    logs: List[Entry]

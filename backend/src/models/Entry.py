from pydantic import BaseModel, Field
from typing import List

class Entry(BaseModel):
    key: int
    payload: str
    creation_datetime: str = Field(
        None,
        title="Creation Datetime",
        format="date-time"
    )
    response_time: int
    response_code: int

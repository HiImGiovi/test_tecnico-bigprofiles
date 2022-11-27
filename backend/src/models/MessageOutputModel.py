from pydantic import BaseModel, Field

class MessageOutputModel(BaseModel):
    status_code: int = Field(
        None,
        title="Status Code",
        description="Status code (numeric)",
        example=200
    )

    message: str = Field(
        None,
        title="string",
        description="Human readable message for understanding",
        example="Ingestion Complete"
    )
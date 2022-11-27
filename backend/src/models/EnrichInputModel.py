from pydantic import BaseModel, Field

class EnrichInputModel(BaseModel):
    key: int = Field(
        None,
        title="Key",
        le=6,
        ge=1,
        description="Id della richiesta (deve essere un numero tra 1 e 6)",
        example="2")
    payload: str = Field(
        None,
        title="Payload",
        max_length=255,
        min_length=10,
        description="Payload della richiesta (una stringa da 10 a 255 caratteri)",
        example="Stringa di esempio"
    )
from pydantic import BaseModel, Field

class EnrichModel(BaseModel):
    key: int = Field(
        None,
        title="Key",
        description="Key of the record"
    )
    creation_datetime: str = Field(
        None,
        title="Creation Datetime",
        description="Data di creazione del log aggregato",
        format="date-time"
    )
    total_response_time_ms: int = Field(
        None,
        title="Total Response Time Ms",
        description="Tempo totale in millisecondi di tutte le risposte inviate nel log aggregato"
    )
    total_requests: int = Field(
        None,
        title="Total request",
        description="Numero totale di tutte le risposte inviate nel log aggregato"
    )
    total_errors: int = Field(
        None,
        title="Total Errors",
        description="Numero totale di tutte le risposte con un errore"
    )
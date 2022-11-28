from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import JSONResponse

from fastapi.security.api_key import APIKey
from src.auth import get_api_key


from src.models import MessageOutputModel, EnrichInputModel
import time
import datetime
import random
from src.db import enrich_inputs_collection

router = APIRouter(
    prefix="/ingest",
)


def write_enrich_input_to_db(key: int, creation_datetime: datetime, payload: str, response_time: int, response_code: int):
    '''
    Summary
    ----------

    Scrive un record a db nella collezione enrich_inputs.

    Parameters
    ----------
    key: int
        Chiave del record variabile da 1 a 6.        
    creation_datetime: datetime
        Data in formato ISO di arrivo della richiesta.
    payload: str
        Payload della richiesta.
    response_time: int
        Tempo di risposta della richiesta.
    response_code: int
        Codice della risposta.

    '''
    enrich_inputs_collection.insert_one({
        "key": key,
        "creation_datetime": creation_datetime,
        "payload": payload,
        "response_time": response_time,
        "response_code": response_code
    })


@router.post("",
             response_model=MessageOutputModel,
             responses={
                 500: {"model": MessageOutputModel, "description": "La richiesta ha riportato un codice 500", "example": {"status_code": 500, "message": "Ingestion Complete"}},
                 200: {"model": MessageOutputModel, "description": "La richiesta ha riportato un codice 200", "example": {"status_code": 200, "message": "Ingestion Complete"}}
             },
             tags=["ingest"],
             operation_id="ingest_api_v1_ingest_post",
             description="Endpoint che permette di andare ad inserire i dati all'interno del sistema. <br />La risposta contiene un messaggio (non interessante) ed un codice (lo stesso che poi viene usato come HTTP_STATUS_CODE).<br />Il codice di risposta è randomico: il **10%** delle risposte hanno un codice 500, le restanti 200.<br />Anche il tempo di risposta è randomico: infatti le risposte possono variare tra **10 ms** e **50 ms** (+-10% di precisione)")
def ingest(enrich_input_model: EnrichInputModel, background_task: BackgroundTasks, api_key: APIKey = Depends(get_api_key)):
    start_time = time.time_ns()
    creation_datetime = datetime.datetime.now()
    response_code = 500 if (random.random() < 0.1) else 200
    response_time_ms = random.randint(10, 50)
    background_task.add_task(write_enrich_input_to_db, enrich_input_model.key,
                             creation_datetime, enrich_input_model.payload, response_time_ms, response_code)
    elapsed_ms = (time.time_ns() - start_time) / 1e6

    # in verità va considerato il tempo di risposta del sistema operativo per far ripartire il thread
    # quindi aspettiamo sempre un tempo maggiore se il sistema non è realtime
    time.sleep((response_time_ms-elapsed_ms)*0.001)

    return JSONResponse({
        "status_code": 500,
        "message": "Ingestion completed"
    }, status_code=500) if (response_code == 500) else {
        "status_code": 200,
        "message": "Ingestion completed"
    }

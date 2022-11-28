from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import os

load_dotenv()

api_key_header_scheme = APIKeyHeader(name="x-api-key")

def get_api_key(
    api_key_header: str = Security(api_key_header_scheme),
):
    '''
    Summary
    -------
    Confronta l'API key con quella salvata nelle variabili di ambiente, e ritorna un exception in caso siano diverse.
    
    Parameters
    ----------
    api_key_header: str 
        L'api-key header della richiesta
    
    Returns
    -------
    L'api-key header della richiesta.

    Exceptions
    ----------
    HTTPException 403 in caso l'API key in entrata sia sbagliata.

    '''
    if api_key_header == os.getenv("API_KEY"):
        return api_key_header
    else:
        raise HTTPException(status_code=403)
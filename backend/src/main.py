from fastapi import FastAPI, HTTPException, Path, Depends, Security, Query, status, BackgroundTasks
from fastapi.security.api_key import APIKeyHeader

from src.routes import ingest, retrieve

import os
from dotenv import load_dotenv


load_dotenv()

api_key_header_scheme = APIKeyHeader(name="x-api-key")

def get_api_key(
    api_key_header: str = Security(api_key_header_scheme),
):
    if api_key_header == os.getenv("API_KEY"):
        return api_key_header
    else:
        raise HTTPException(status_code=403)

app = FastAPI()
@app.get("/" )
def home():
    return{"ciao":"bella"}
app.include_router(ingest.router, prefix="/api/v1")
app.include_router(retrieve.router, prefix="/api/v1")


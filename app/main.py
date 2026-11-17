from fastapi import FastAPI,  status, Request
from fastapi.security import APIKeyHeader
from datetime import datetime, timezone 
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os
import hashlib

app = FastAPI()
load_dotenv()
secret_key = os.getenv("SECRET_KEY")
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

class log_recebido(BaseModel):
    batch: dict[str, list[str]]
#    token: str

class log_padronizado(BaseModel):
    #TimeStamp_API : str
    raw_log: str
    servico: str
    nome_pattern: str

"""
TimeStamp:    [Mon Dec 05 05:50:50 2032] 
Log:          [notice] workerEnv.init() ok /etc/httpd/conf/workers2.properties'
Serviço:      'Apache'
Nome_pattern: 'teste-2'
"""

@app.post("/",response_model=list[log_padronizado])
def recebe_log(log: log_recebido):
    hash_api_key = hashlib.sha256(secret_key.encode("utf-8")).hexdigest()
    resultado = [] 

    try:
        timestamp_atual = datetime.now(timezone.utc).isoformat()
        for post_batch in log.batch:
            padronizado = {
                "TimeStamp_API": timestamp_atual,
                "raw_log": log.batch[post_batch][0],
                "servico": log.batch[post_batch][1],
                "nome_pattern": log.batch[post_batch][2]
            }
            resultado.append(padronizado)

        print(resultado)
        return resultado

    except Exception as error:
        print(f"Erro: {error}")

@app.get("/")
def ler_log():
    return {"status":"online", "nome":"LogRelay"}

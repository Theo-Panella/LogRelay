from fastapi import FastAPI,  status, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from datetime import datetime, timezone 
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os
import hashlib
import secrets
import hashlib
import hmac

app = FastAPI()
load_dotenv()
secret_key = os.getenv("SECRET_KEY")
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)
api_assinatura_header = APIKeyHeader(name="Signature", auto_error=False)

class log_recebido(BaseModel):
    batch: dict[str, list[str]]

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

async def verify_auth(key: str = Security(api_key_header)) -> str:
    if not key or not secrets.compare_digest(key, secret_key):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API Key",
        )
    return key

@app.post("/",response_model=list[log_padronizado])
async def recebe_log(log: log_recebido, api_key: str = Depends(verify_auth)):
    resultado = [] 

    try:
        assinatura = hmac.new(secret_key, log, hashlib.sha256).hexdigest()
        if hmac.compare_digest(assinatura,api_assinatura_header):
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
            print(api_key_header)
            return resultado
        else:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing HMAC authentication",
            )

    except Exception as error:
        print(f"Erro: {error}")

@app.get("/")
def ler_log():
    return {"status":"online", "nome":"LogRelay"}
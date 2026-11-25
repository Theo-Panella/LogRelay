from fastapi import FastAPI,  status, HTTPException, Depends, Security, Header, Request
from fastapi.security import APIKeyHeader
from datetime import datetime, timezone
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import hashlib
import hmac

load_dotenv() 

if not os.getenv("SECRET_KEY"):
    print("=="*10)
    print("Impossivel subir a API, verifique a secret key no .env e tente novamente")
    print("=="*10)
    raise SystemExit()

app = FastAPI()
secret_key = os.getenv("SECRET_KEY")
api_assinatura_header = APIKeyHeader(name="Signature", auto_error=False)

class log_recebido(BaseModel):
    batch: dict[str, list[str]]

class log_padronizado(BaseModel):
    TimeStamp_API : str
    raw_log: str
    servico: str
    nome_pattern: str

"""
TimeStamp:    [Mon Dec 05 05:50:50 2032] 
Log:          [notice] workerEnv.init() ok /etc/httpd/conf/workers2.properties'
Serviço:      'Apache'
Nome_pattern: 'teste-2'
"""

async def verify_auth(request: Request, assinatura_header: str = Security(api_assinatura_header)) -> None:
    if not assinatura_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Assinatura HMAC vazia",
        )
    corpo_bruto = await request.body()
    assinatura_esperada = hmac.new(secret_key.encode("utf-8"), corpo_bruto, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(assinatura_esperada,assinatura_header):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Assinatura HMAC inválida"
        )

async def integridade_batch(log: log_recebido):
    for campo in log.batch:
        if len(log.batch[campo]) != 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Campos insuficientes"
            )
    return "ok"

@app.post("/",response_model=list[log_padronizado], dependencies=[Depends(verify_auth)])
async def recebe_log(log: log_recebido, ib: str = Depends(integridade_batch)):
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
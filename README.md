# LogRelay

API simples para receber e processar logs padronizados.

## Funcionalidades

- Recebimento de logs em lote
- Padronização de formato de logs
- Suporte a múltiplos serviços

## Instalação

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

```bash
uvicorn main:app --reload
```

## Endpoints

- `POST /` - Recebe logs em lote
- `GET /` - Verifica status da API

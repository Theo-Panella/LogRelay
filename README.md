# LogRelay

API simples para receber e processar logs padronizados.

## Funcionalidades

- Recebimento de logs em lote
- Padronização de formato de logs
- Suporte a múltiplos serviços

## Instalação

### Sem Docker
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Com Docker
```bash
docker-compose build
docker-compose up
```

A API estará disponível em `http://localhost:8000`

## Uso

### Sem Docker
```bash
uvicorn main:app --reload
```

### Com Docker
A API inicia automaticamente quando você executa `docker-compose up`

## Comunicação com o Agent (Docker)

Este projeto roda como um serviço chamado `web` em um container Docker. Se você tem um `agent` em outro projeto que precisa se comunicar com esta API:

```bash
docker network connect public web
docker network connect public agent
```

Isso conecta ambos os containers à mesma rede Docker chamada `public`, permitindo que um acesse o outro via hostname. Agora:
- Do agent, você acessa a API usando: `http://web:8000`
- A resolução de DNS funciona automaticamente dentro da rede Docker

## Endpoints

- `POST /` - Recebe logs em lote
- `GET /` - Verifica status da API

## TODO
- [ ] Usar TLS na comunicação
- [x] Usar HMAC como verificador de autenticidade
- [ ] Implementar JWT
- [x] Corrigir HMAC no teste.py: importar `hmac` e assinar bytes (`secret_key.encode()` e `json.dumps(payload).encode()`)
- [x] Corrigir HMAC no main.py: calcular a assinatura sobre o corpo bruto (`await request.body()`) com a chave em bytes
- [x] Ler o header `Signature` via `Security(api_assinatura_header)` em vez de comparar com o objeto `APIKeyHeader`
- [x] Falhar na inicialização se `SECRET_KEY` não estiver definida (`load_dotenv()` antes da verificação)
- [x] Adicionar `TimeStamp_API` ao modelo `log_padronizado` (hoje é descartado pelo `response_model`)
- [x] Validar o formato do batch (3 campos) para evitar `IndexError`
- [x] Parar de enviar a chave no header `Authorization` quando o HMAC estiver funcionando
- [x] Remover os `print` que exibiam a assinatura esperada no log

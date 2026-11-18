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
- [x] Autenticação de requisição por comparação de chave API
- [ ] Usar TLS na comunicação
- [ ] Usar HMAC como verificador de autenticidade
- [ ] Implementar JWT
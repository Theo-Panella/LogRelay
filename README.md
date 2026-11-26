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

## Segurança

### Autenticação das requisições

O `POST /` exige dois headers:

- `TimeStamp`: data e hora do envio em ISO 8601 **com fuso horário** (ex.: `datetime.now(timezone.utc).isoformat()`)
- `Signature`: HMAC-SHA256, em hexadecimal, calculado com a `SECRET_KEY` sobre `corpo_bruto + TimeStamp` (ambos em UTF-8)

A requisição é recusada com `401` se algum header faltar, se o `TimeStamp` for inválido ou não tiver fuso horário, se ele estiver a 5 minutos ou mais do relógio do servidor (para trás ou para frente), ou se a assinatura não bater. Veja `teste.py` para um exemplo de cliente.

### TLS

A API fala **HTTP puro**, sem TLS. Criptografar o tráfego é responsabilidade de quem faz o deploy: coloque a API atrás de um proxy reverso com HTTPS (nginx, Caddy, Traefik etc.) ou rode o uvicorn com `--ssl-keyfile` e `--ssl-certfile`. Sem TLS, qualquer um na rede consegue ler os logs enviados.

### Limites do HMAC

O HMAC garante que a requisição veio de alguém que conhece a `SECRET_KEY` e que o corpo e o `TimeStamp` não foram alterados. Ele **não** garante:

- **Confidencialidade:** o corpo continua legível na rede. Para isso, use TLS.
- **Identificação de cada cliente:** todos os clientes usam a mesma chave. Não dá para saber qual deles enviou a requisição, nem revogar o acesso de um só. Se a chave vazar, ela precisa ser trocada em todos.
- **Proteção contra replay:** uma requisição capturada pode ser reenviada até a janela de 5 minutos expirar (ver TODO).
- **Proteção do resto da requisição:** só o corpo e o `TimeStamp` entram na assinatura. Método, caminho e os demais headers não são assinados.

Os relógios do cliente e do servidor também precisam estar sincronizados (NTP). Uma diferença de 5 minutos ou mais faz todas as requisições serem recusadas.

## TODO
- [ ] Bloquear replay dentro da janela de 5 minutos (guardar as assinaturas já usadas até expirarem e recusar as repetidas)
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

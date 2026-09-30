# Telemetria Energética

API REST para registrar e acompanhar o consumo energético de máquinas. A aplicação usa FastAPI, SQLAlchemy e SQLite por padrão.

## Requisitos

- Python 3.11 ou superior
- Poetry

## Instalação

Na raiz do projeto, instale as dependências e crie o ambiente virtual:

```bash
poetry install
```

## Executar a API

```bash
poetry run task run
```

A API ficará disponível em <http://127.0.0.1:8000>. A documentação interativa do OpenAPI fica em <http://127.0.0.1:8000/docs>; a documentação ReDoc, em <http://127.0.0.1:8000/redoc>.

Por padrão, os dados são persistidos em `telemetria.db` no diretório de execução. Para usar outro banco, configure a variável de ambiente `DATABASE_URL` antes de iniciar a aplicação.

## Testes

Execute a suíte com relatório de cobertura:

```bash
poetry run task test
```

Ou execute os testes diretamente:

```bash
poetry run pytest
```

Os testes usam um banco SQLite em memória e não dependem do banco de desenvolvimento.

## API

### Medições

| Método | Rota | Descrição |
| --- | --- | --- |
| `POST` | `/medicoes/` | Registra uma medição; retorna `201 Created`. |
| `GET` | `/medicoes/` | Lista as medições em ordem de criação. |
| `PUT` | `/medicoes/{medicao_id}` | Atualiza os dados de uma medição. |
| `DELETE` | `/medicoes/{medicao_id}` | Remove uma medição. |
| `GET` | `/medicoes/kpis` | Retorna indicadores de consumo. |

O corpo usado para criar ou atualizar uma medição é:

```json
{
  "maquina_id": 1,
  "consumo_kwh": 12.5,
  "status": "operando"
}
```

O campo `status` aceita `operando`, `manutencao` ou `desligado`. O identificador e a data/hora são preenchidos pela aplicação e pelo banco. As rotas de atualização e remoção retornam `404 Not Found` quando o identificador não existe.

### Indicadores

`GET /medicoes/kpis` retorna o consumo total, o consumo médio e a quantidade de medições com status `operando`:

```json
{
  "consumo_total_kwh": 32.5,
  "consumo_medio_kwh": 16.25,
  "maquinas_operando": 1
}
```

O endpoint `/` retorna uma mensagem indicando que a API está ativa. Os detalhes dos contratos e os exemplos de requisição também estão disponíveis em `/docs` enquanto a aplicação estiver em execução.

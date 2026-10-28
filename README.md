# SAI DA JSON

API desenvolvida em Python com FastAPI para receber mensagens de usuários, interpretar dados escolares com a Gemini AI e registrar notas em memória.

## Visão geral

Este projeto cria um backend simples para:

- receber mensagens em texto;
- extrair automaticamente informações como nome do aluno, disciplina e nota;
- confirmar o cadastro da nota em uma resposta amigável;
- listar os alunos cadastrados;
- expor uma documentação interativa via Swagger/OpenAPI.

A aplicação usa:

- Python
- FastAPI
- Pydantic
- Google GenAI (Gemini)
- python-dotenv

## Funcionalidades

- `POST /api/chat`: recebe uma mensagem e tenta extrair os dados do aluno.
- `GET /api/alunos`: retorna a lista de alunos cadastrados em memória.
- `GET /`: redireciona para a documentação da API (`/docs`).
- Documentação automática com Swagger em `/docs`.

## Estrutura do projeto

```text
.
├── .gitignore
├── README.md
├── server.py
└── .env
```

## Pré-requisitos

- Python 3.10+
- Conta e chave da API Gemini
- Pip instalado

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/LucianaBritoDev/saidajson-main.git
cd saidajson-main
```

2. Crie um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

3. Instale as dependências:

```bash
pip install fastapi uvicorn python-dotenv google-genai pydantic
```

## Configuração de ambiente

Crie um arquivo `.env` na raiz do projeto com sua chave da API Gemini:

```env
GEMINI_API_KEY=sua_chave_aqui
```

## Execução

Inicie a aplicação com:

```bash
uvicorn server:app --reload
```

A API estará disponível em:

- http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs

## Endpoints

### GET /api/alunos

Retorna a lista de alunos cadastrados em memória.

Exemplo de resposta:

```json
{
  "alunos": [
    {
      "nome_aluno": "Maria Souza",
      "disciplina": "Matemática",
      "nota": 9.5
    }
  ]
}
```

### POST /api/chat

Recebe uma mensagem do usuário e tenta extrair:

- nome do aluno;
- disciplina;
- nota;
- resposta final amigável.

Exemplo de corpo da requisição:

```json
{
  "mensagem": "Registre a nota 9.5 da aluna Maria Souza em Matemática."
}
```

Exemplo de resposta:

```json
{
  "status": "Nota cadastrada com sucesso.",
  "dados_extraidos": {
    "nome_aluno": "Maria Souza",
    "disciplina": "Matemática",
    "nota": 9.5
  },
  "resposta_final": "Nota registrada com sucesso para Maria Souza na disciplina de Matemática."
}
```

Se algum dado estiver ausente ou ambíguo, a API responde informando quais informações precisam ser esclarecidas.

## Observações

- Os dados dos alunos são armazenados em memória durante a execução da aplicação.
- A aplicação não persiste registros em banco de dados.
- A resposta da IA é validada conforme o schema `CadastroNotasSchema`.

## Licença

Este projeto não possui uma licença definida no repositório.

## Autor

Luciana Brito

# CatAPI

Este é um CRUD básico para informações sobre raças de gatos, construído com o uso do framework FastAPI.

### Tecnologias utilizadas

- Python 3.8

- FastAPI 0.6

- SQLAlchemy 1.4

- Pytest 5.4

### Como inicializar o projeto

Após clonar o projeto e criar o ambiente virtual, execute os seguintes comandos na raiz do projeto:

        pip install -r requirements.txt

        uvicorn api.main:app --reload

### Documentação

A documentação dos endpoints pode ser acessado acessando:

<BASE_URL>/docs

<Base_URL>/redoc

### Testes

O testes se encontram na pasta 'tests'. Para executá-los, execute o comando abaixo na raiz do projeto.

        pytest -vv .

### Logs

Toda requisição feita à API é salva no arquivo 'registered_logs' que é criado no momento da inicialização da aplicalção no diretório '/.api/logs'
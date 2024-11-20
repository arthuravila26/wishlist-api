# Wishlist API

A API WishList permite que os usuarios possam adicionar items em sua lista de desejo de produtos que queram comprar no futuro.

# Como Executar

A API permite que a aplicação seja executada de 2 formas, utilizando o ambiente docker ou rodando o script no terminal para iniciar a aplicação.

### Rodando Localmente sem Docker
Para rodar fora do ambiente docker, é importante frizar que é preciso da instalação de algumas ferramentas:

- Python 3.12
- Pip 3.x
- Postgres

Para executar a mesma, siga os passos:

1 - É recomendado que crie um ambiente virtual para que as libs usadas não interfiram no sistema operacional da sua maquina. Para isso, execute os seguintes comandos.
- `python3 -m venv venv`
- `source venv/bin/activate`
2 - Após a ativação do ambiente virtual, execute o comando para instalar os requerimentos necessarios para a aplicação usitilizando o comando `pip3 install -r requirement.txt`
3 - No terminal aonde será executado a aplicação, exporte as variaveis de ambiente do arquivo `env`
4 -  Após esse procedimento, a API estará pronta para uso e para executar, rode o comando `python3 run.py`. Esse comando ira iniciar o coordinator da aplicação aonde executara o servidor uvicorn.

### Rodando apartir de do container
O container é um ambiente isolado aonde podemos facilitar o desenolvimento e a execução da aplicação. Este projeto conta com um `docker-compose.yml` qual conta com o serviço de banco de dados e da API propriamente dita.
Este docker compose realiza o build da imagem da api junto com suas variaveis de ambiente.
Para executar o docker compose apenas precisamos executar o comando `docker compose up` e isso ira iniciar a API e o banco de dados.

# Endpoints

O framework FastAPI prove uma documentação automatica da nossa aplicação, criando um swagger a partir das rotas q são criadas. Isso facilita para verificarmos todas as rodas, endpoints e o body que precisamos usar na request.
A documentação pode ser acessada via `localhost:8000/docs`. Importante frizar que a aplicação precisa esta rodando para ter acesso a documentação.

# Autenticação e Autorização

A Wishlist API conta com sistema de autenticação e autorização com uso de senha e JWT Token.
Ao inciar, é preciso criar um usuário com nome, email e senha. A partir desse dado, é possivel gerar um JWT Token com o email e senha pelo endpoint `/api/token`. Com esse token, será possivel acessar os outros endpoints da aplicação. Este token tem duração 30 minutos.

# TODO
Ainda é necessario criar testes para a aplicação.
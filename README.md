# Wishlist API

A API WishList permite que os usuarios possam adicionar items em sua lista de desejo de produtos que queram comprar no futuro.

# O Projeto
Este repositorio conta com 2 APIs. A primeira se trata da API de products, a qual disponibiliza um CRUD para criação de produtos para a API de wishlist os produtos de acordo com o ID. A segunda é a API de wishlist, esta API possui o CRUD de usuário
e tambem, a lógica de negocio da wishlist. Ambas são serviços separados e independentes que se comunicam utilizando o docker-compose na mesma rede.

# Rodando apartir de do container
O container é um ambiente isolado aonde podemos facilitar o desenolvimento e a execução da aplicação. Este projeto conta com um `docker-compose.yml` na raiz do projeto, qual conta com o serviço de banco de dados
API de products e da API de wishlist.
Este docker compose realiza o build da imagem da api junto com suas variaveis de ambiente.
Para executar o docker compose apenas precisamos executar o comando `docker compose up` e isso ira iniciar as APIs e o banco de dados.

# Endpoints
## Wishlist-API
O framework FastAPI prove uma documentação automatica da nossa aplicação, criando um swagger a partir das rotas q são criadas. Isso facilita para verificarmos todas as rodas, endpoints e o body que precisamos usar na request.
A documentação pode ser acessada via `localhost:8000/docs`. Importante frizar que a aplicação precisa esta rodando para ter acesso a documentação.

## Products-API
A API de products foi criada utilizando a linguagem Go e o framework GIN para criar uma API que disponibiliza um CRUD para os products que seram usados na API de wishlist. A API de products conta com os endpoints abaixi:
- `GET /products`: Responsavel por trazer todos os produtos cadastrados no banco de dados.
- `GET /product/:id`: Responsavel por trazer um produto especifico cadastrados no banco de dados.
- `DELETE /product/:id`: Deleta um produto especifico cadastrados no banco de dados.
- `PATCH /product/:id`: Atualiza um produto especifico cadastrados no banco de dados.
- `POST /products`: Responsavel por criar produtos no banco de dados utilizando a seguinte estrutura:
```commandline
{
    "price": float,
    "image": string,
    "brand": string,
    "title": string,
    "reviewScore": float
}
```

# Autenticação e Autorização

A Wishlist API conta com sistema de autenticação e autorização com uso de senha e JWT Token.
Ao inciar, é preciso criar um usuário com nome, email e senha. A partir desse dado, é possivel gerar um JWT Token com o email e senha pelo endpoint `/api/token`. Com esse token, será possivel acessar os outros endpoints da aplicação. Este token tem duração 30 minutos.

# Testes Unitarios

Foram criados testes unitarios para garantir a qualidade das operações do CRUD de usuario e tambem da logica da wishlist.
Para executar os testes, é preciso acessar a pasta `whishlist-api` e rodar o comando `python -m unittest`
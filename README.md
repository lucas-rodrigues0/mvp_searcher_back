# MVP Searcher
## Back-end

Projeto de MVP realizado para o curso de Pós graduação em Engenharia de Software da universidade Puc RJ.


### Objetivos

Com o objetivo de difundir o conhecimento aos direitos e deveres dos brasileiros, esse projeto vem a oferecer um pesquisador de texto completo para a Constituição Federal de 1988.

Também oferece uma sessão de comentários para a troca de conhecimento entre os usuários.

Esse projeto é um MVP e pretende evoluir para que, tanto o pesquisador de texto quanto a sessão de comentário, possam desenvolver novas funcionalidades que irão melhorar a busca de texto e ampliar a sessão de comentários, para que usuários possam trocar conhecimento respondendo a comentários existentes, inserir outros conteúdos além de texto.  


### Tecnologias utilizadas

- [Python](https://www.python.org/)
- [Flask-openapi3](https://luolingchun.github.io/flask-openapi3/v3.x/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Whoosh](https://whoosh.readthedocs.io/en/latest/index.html)
- [PyPDF2](https://pypdf2.readthedocs.io/en/3.x/)
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/)


## Instruções para rodar o projeto

Fazer o download do projeto e seguir os passos a seguir.

### Set-up inicial:

- Na raiz do projeto, criar um ambiente virtual Python para a instalação das dependências.

```
python3 -m venv .venv
```
 
- Ativar o ambiente virtual.

```
source .venv/bin/activate
```

- Instalar as dependencias do projeto.

```
pip install -r requirements.txt
```

### Criação do banco de dados:

- Criar um database no banco postgres. Pode criar o database com um nome diferente, mas colocar o nome do database no arquivo `.env` especificando o acesso ao database criado. O nome sugerido é "searcher".

- Pelo comando `psql` do postgres.

```
CREATE DATABASE searcher;
```

- Para maiores informações de como instalar e criar um database, clique aqui para a documentação do PostgreSQL: 
    - [Instalação](https://www.postgresql.org/docs/current/tutorial-install.html)
    - [Criar database](https://www.postgresql.org/docs/current/tutorial-createdb.html)


- Depois de criado o database, adicionar as configurações necessárias para o acesso ao banco de dados.

- Criar o arquivo `.env` com as configuração de acesso ao banco de dados. Pode utilizar o arquivo `env.sample`, duplicando o arquivo e renomendo para .env com as devidas variáveis pedidas.

- Executar o script para a criação das tabelas no db.

```
python create_tables.py 
```

### Indexação do arquivo PDF:

- Executar o script para a indexação do arquivo PDF utilizado na aplicação.

```
python pdf_indexation.py 
```

- No console deverá ser apresentado 264 páginas com o status OK. Caso já houver feito o index, esse será sobre-escrito pela nova execução.
O conteúdo das páginas só será inserido no db caso ainda não esteje salvo. Caso já exita no db, será apresentado uma messagem informando que as páginas já existem. 


### Execução da aplicação:

- Para rodar a aplicação, executar o comando
```
python app.py
```


## Funcionalidades

### Rotas da API
O projeto apresenta uma API com a seguintes rotas:

- *__/account/register__*  
Registro de usuário na base de dados  
Método da requisição: "POST"  
Header Content-Type da requisição: "application/json"  
Header Authorization: Não é necessário  
Payload da requisição: json com as chaves email, username e password  
Resposta da requisição: json com as chaves token e account_id  

- *__/account/login__*  
Validação de usuário já cadastrado na base
Método da requisição: "POST"  
Header Content-Type da requisição: "application/json"  
Header Authorization: Não é necessário  
Payload da requisição: json com as chaves email e password  
Resposta da requisição: json com as chaves token e account_id  

- *__/comments__*  
Leitura e inserção de comentários de usuários cadastrados  
Método da requisição: "GET" ou "POST"  
Header Content-Type da requisição: "application/json"  
Header Authorization: Necessário somente para o método POST   
Payload da requisição: json com a chave content  
Resposta da requisição: Lista de dicionarios com as chaves comment_id, account_id, username, content e created_at  

- *__/searcher__*  
Acesso ao pesquisador de texto completo da Contituição Federal  
Método da requisição: "GET"  
Header Content-Type da requisição: "application/json"  
Header Authorization: Necessário  
Query Parameter: chave `query` com os termos da busca  
Resposta da requisição: Dicionário com os resultados das paginas encontradas como chave, e da amostragem de conteúdo como valor  


### Autenticação

A autenticação de usuário cadastrado na base de dados é feita pelo token JWT.  
O token enviado no momento da autenticação ou do registro de novo usuário é salvo no Session Storage do browser. Portanto caso a sessão for terminada (a janela ou aba forem fechados), será necessário refazer a autenticação para obter o token novamente.


### Full-text search

O buscador de texto funciona a partir da indexação do conteúdo de texto do arquivo PDF com a Constituição Federal.  
A biblioteca Whoosh é utilizada para realizar essa indexação e a busca pelos termos.  
A indexação é feita para cada página do arquivo, permitindo assim identificar em quais páginas os termos foram encontrados, e assim facilitar a leitura do conteúdo no próprio PDF.  

O contéudo textual das páginas do PDF estão sendo inseridos na base de dados.  
Apesar de nesse MVP, esses dados salvos não estão sendo utilizados, essa estrutura visa, num desenvolvimento próximo, melhorar a indexação e a busca do conteúdo, subdividindo o conteúdo de cada página do PDF nos Títulos, Capitulos e Artigos em que a Constituição Federal é composta.

### Documentação

o `Flask openapi3` traz o `swagger`, `redoc` e `rapidoc` para a automatização da documentação técnica da API.

A rota home da API `"/"` está redirecionando para a opção dessas documentações fornecidas pelo Flask openapi3.
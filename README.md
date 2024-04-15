# mvp_searcher_back

projeto de mvp realizado para o curso de Pós graduação em Engenharia de Software da universidade Puc RJ


### Set-up inicial

criar o ambiente virtual Python para a instalação das dependências

```
python3 -m venv .venv
```

Ativar o ambiente virtual
```
source .venv/bin/activate
```

Instalar as dependencias do projeto
```
pip install -r requirements.txt
```

### Criação do banco de dados

Criar um database no banco postgres. Pode criar o database com um nome diferente, mas colocar o nome do database no arquivo `.env` especificando o acesso ao database criado. O nome sugerido é "searcher"

pelo comando do Psql
```
CREATE DATABASE searcher;
```

Criar o arquivo `.env` com as configuração de acesso ao banco de dados. Pode utilizar o arquivo `env.sample`, duplicando o arquivo e renomendo para .env com as devidas variáveis pedidas

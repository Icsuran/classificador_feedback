# Alumind

## Cenário
A AluMind é uma startup que oferece um aplicativo focado em bem-estar e saúde mental, proporcionando aos usuários acesso a meditações guiadas, sessões de terapia, e conteúdos educativos sobre saúde mental. Com o alto crescimento da base de usuários, a AluMind está começando a ter gargalos para analisar feedbacks vindo dos usuários em diferentes plataformas (canais de atendimento ao cliente; comunidades no Discord; redes sociais). Portanto, nessa tarefa, você criará uma aplicação cuja responsabilidade seja de analisar os feedbacks vindos dos usuários, classificá-los a partir do seu sentimento e elencar as possíveis melhorias contidas neles.

Utilizei PostgreSQL, Postman, Linux Mint, Python, Flask, Jinja, Bootstrap, smtplib, Templates, Psycopg, openai, lagnchain e etc.

## Base da dados PostgreSQL

* Você precisa, antecipadamente, ter o SGBD PostgreSQL instalado
* o script de criação da base de dados da aplicação está em **database.sql** 
* os parâmetros de conexão estão no arquivo de configuração **config.ini**
* No Linux, abra o terminal e acesse o PostgreSQL executando o seguinte comando:
```
psql -h localhost -U postgres
```
* Em seguida, importe a base de dados via script **database.sql**

```
\i database.sql
```
## Execução

Uma vez criada a base de dados, basta abrir o projeto em sua IDE de preferência (ex: VSCode) e digite no terminal:
```
pip install -r requirements.txt 
```
* Este comando irá instalar todas os pacotes necessários.
* confira os parâmetros de conexão ao banco de dados no arquivo config.ini 
* Depois, execute no terminal o comando que inicializa a aplicação:
```
flask --app main run --debug
```
Obs: No config.ini é possível escolher entre acessar o LLM diretamente pela api da OpenAI ou via LangChain. O padrão é está langchain.

## ***Endpoint*** que recebe novos feedbacks:

* Há um exemplo de rota em **allura.json** que pode ser importado no Postman.
* No Postman a rota deve seguir formatação e parâmetros exigidos pela aplicação:
```json
POST /feedbacks Content-Type: application/json
{ "id": "4042f20a-45f4-4647-8050-139ac16f610b", "feedback": "Gosto muito de usar o Alumind! Está me ajudand o bastante em relação a alguns problemas que tenho. Só quer ia que houvesse uma forma mais fácil de eu mesmo realizar a edição do meu perfil dentro da minha conta" }
```

* O ***endpoint*** deve ser acessado por POST
* Uma vez analisado, o mesmo feedback (com mesmo identificador) não poderá ser novamente analisado já que defini o id como pk.
* dica: Para gerar novos id's para os feedbacks dos clientes, basta gerar no próprio Python: 
```
import uuid
str(uuid.uuid4())
```
* Desenvolvi também uma página web alternativa que pode ser acessada por http://localhost:5000/ que é capaz também de receber novos feedbacks - mas desta vez através de um formulário html. Neste caso, os id's são gerados dinamicamente (sem a necessidade do usuário/cliente se preocupar de enviar também o id juntamente de seu feedback). A cada refresh no navegador um novo id é gerado. 

## ***Endpoint***  que exibe a página web de relatório:

* Deve ser acessado pelo navegador pelo endereço http://localhost:5000/relatorio

* Usei aqui Flask, Psycopg, html, Jinja (template html) e para estilo CSS a biblioteca Bootstrap

## ***Endpoint***  que envia um email com o resumo semanal:

* http://localhost:5000/resumo_semanal

* Há um exemplo de rota em **allura.json** que pode ser importado no Postman.
* Pode ser acessado tanto pelo navegador como também pelo Postman
* O endpoint deve ser acessado por GET
* Para testar, recomendo trocar o parâmetro **To** (email de destinatário) presente no arquivo de configuração **config.ini**. Este será o email que recebera o resumo da semana.

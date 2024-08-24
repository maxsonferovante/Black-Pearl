

# Black Pearl

O Sistema de Gestão de Convênios do Sindicato dos Portuários do Pará e Amapá é uma solução robusta criada utilizando o Framework Django em conjunto com o banco de dados PostgreSQL.

Ele oferece funcionalidades abrangentes, incluindo o cadastro detalhado de associados e seus respectivos dependentes. Além disso, permite o gerenciamento completo de planos de saúde, odontológicos e cartões de convênios, abrangendo desde a inclusão até a atualização dos dados.

A plataforma também oferece um controle eficaz de faturas e pagamentos, facilitando o acompanhamento e a organização financeira. Além disso, gera relatórios detalhados que fornecem uma visão ampla e completa do sistema, auxiliando na tomada de decisões estratégicas.

É uma solução integrada e eficiente, centralizando todas as operações relacionadas aos convênios, proporcionando ao Sindicato dos Portuários uma gestão ágil, precisa e transparente de suas atividades.


## Demonstração

No link uma Demonstração da tela em que são listados todos os associados cadastrados.

https://photos.app.goo.gl/CemnDK5JNCGGaBc67

## Etiquetas

Adicione etiquetas de algum lugar, como: [shields.io](https://shields.io/)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)


## Autores

- [@maxsonferovante](https://github.com/maxsonferovante)

## Usado por

Esse projeto é usado pela seguinte empresa:

- Sindicato dos Portuários do Pará e Amapá



## Funcionalidades

- Gerenciamento de Associados e seus Dependentes
- Gerenciamento de Convenios (Cartões de Convênio, Plano de Saude, e Plano Odontologico)
- Gerenciamento de Cobranças em faturas dos convenios

## Uso/Instalação

Para clonar e rodar esse projeto, você precisará ter o [Git](https://git-scm.com) e o [Python](https://www.python.org/) instalados em seu computador. A partir da sua linha de comando:

```bash
    git clone https://github.com/maxsonferovante/Black-Pearl.git
    cd Black-Pearl
```

Para instalar e configurar o ambiente virtual:

```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
```
Antes da execução, crie o arquivo para as variáveis de ambiente:

```bash
    touch .env
```
O conteúdo do arquivo .env deve ser:

```bash
    SECRET_KEY = 'your_secret_key'
    DB_ENGINE = 'django.db.backends.postgresql_psycopg2'
    DB_NAME = 'your_db_name'
    DB_USER = 'your_db_user'
    DB_PASSWORD = 'your_db_password'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
```

Para rodar o projeto:
```
    python manage.py makemigrations && python manage.py migrate
```
```bash
    python manage.py runserver
```


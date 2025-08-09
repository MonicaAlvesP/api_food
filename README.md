# 🍽️ Api Food

## 📝 Descrição

A **api_food** é uma API REST desenvolvida em Python utilizando o framework FastAPI, com autenticação via JWT, que permite o gerenciamento de um catálogo de alimentos. Ela possibilita o cadastro, atualização, listagem e remoção de itens alimentícios, sendo ideal para sistemas de cardápio digital, delivery ou controle de estoque de restaurantes.

## ✨ Funcionalidades

- **🔐 Autenticação JWT:** Apenas usuários autenticados (admin) podem cadastrar, editar ou remover alimentos.
- **👀 Listagem pública:** Qualquer usuário pode consultar a lista de alimentos disponíveis.
- **📋 CRUD de alimentos:** Permite criar, atualizar, listar e deletar alimentos, cada um com nome, tipo, preço e imagem.
- **💾 Persistência em banco de dados SQLite** usando SQLAlchemy.

## 🛠️ Endpoints principais

- `GET /foods` — 📄 Lista todos os alimentos (público)
- `POST /foods` — ➕ Adiciona um novo alimento (requer autenticação)
- `PUT /foods/{food_id}` — ✏️ Atualiza um alimento existente (requer autenticação)
- `DELETE /foods/{food_id}` — 🗑️ Remove um alimento (requer autenticação)
- `POST /token` — 🔑 Gera o token de autenticação

## 🚀 Como executar

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Execute a aplicação:

```bash
uvicorn app.main:app --reload
```

3. Acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🔒 Configuração do arquivo .env

Crie um arquivo chamado `.env` na raiz do projeto com o seguinte conteúdo:

```
SECRET_KEY=sua_chave_secreta_forte_aqui
ADMIN_PASSWORD=sua_senha_forte_aqui
```

- `SECRET_KEY`: Uma string longa e única para assinar os tokens JWT.
- `ADMIN_PASSWORD`: A senha do usuário admin (será armazenada de forma segura no sistema).

**Nunca compartilhe ou suba o arquivo `.env` para repositórios públicos!**

## ⚠️ Observações

- 👤 Usuário padrão: `admin` / senha: `adminpassword`
- 🗃️ O banco de dados utilizado é SQLite, criado automaticamente na raiz do projeto.
- 🏭 Para produção, recomenda-se utilizar hash de senha e variáveis de ambiente para a chave secreta.

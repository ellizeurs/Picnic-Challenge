# Ticket Categorizer API

Esta é uma API para categorização automática de tickets de suporte usando embeddings de texto com o modelo **MiniLM** (`all-MiniLM-L6-v2`). O objetivo é sugerir categorias para tickets, ajudando o gerente de suporte a identificar problemas importantes.

---

## 🛠️ Setup

1. Clone o repositório:

```bash
git clone <REPO_URL>
cd <PASTA_DO_PROJETO>
````

2. Crie um ambiente virtual:

`````bash
python -m venv venv
`````

3. Ative o ambiente virtual:

* Windows:

`````bash
venv\Scripts\activate
`````

* Linux / MacOS:

`````bash
source venv/bin/activate
`````

4. Instale as dependências:

`````bash
pip install -r requirements.txt
`````

5. Inicie a aplicação:

`````bash
uvicorn app.main:app --reload
`````

A API ficará disponível em: `http://127.0.0.1:8000`

---

## 📌 Rotas

### 1. Rota raiz

#### GET /

**Descrição:** Verifica se a API está rodando.

**Resposta:**

`````json
{
  "message": "Ticket categorizer API running"
}
`````

---

### 2. Listar todos os tickets com categoria sugerida

#### GET /tickets

**Descrição:** Retorna todos os tickets com a categoria sugerida baseada em embeddings.

**Resposta (exemplo):**

`````json
[
  {
    "ticket_id": 1,
    "subject": "Account locked after too many tries",
    "suggested_category": "Login"
  },
  {
    "ticket_id": 2,
    "subject": "Return request for ORD-2025-2002",
    "suggested_category": "Returns"
  }
]
`````

---

### 3. Obter ticket específico

#### GET /tickets/{ticket_id}

**Parâmetro:**

* `ticket_id` (int): ID do ticket.

**Descrição:** Retorna o ticket solicitado, seus comentários e a categoria sugerida.

**Resposta (exemplo):**

`````json
{
  "ticket_id": 1,
  "subject": "Account locked after too many tries",
  "comments": [
    "Locked out after multiple attempts. Can you unlock my account? 🙏",
    "Hey Marcus, I updated your 2FA to email for now..."
  ],
  "suggested_category": "Login"
}
`````

---

### 4. Listar categorias com quantidade de tickets

#### GET /categories

**Descrição:** Retorna todas as categorias sugeridas e a quantidade de tickets que se encaixam em cada uma.

**Resposta (exemplo):**

`````json
[
  {
    "category": "Login",
    "count": 5
  },
  {
    "category": "Returns",
    "count": 12
  },
  {
    "category": "Orders",
    "count": 8
  }
]
`````

---

## ⚡ Observações

* As categorias são sugeridas automaticamente usando embeddings de texto (`sentence-transformers`) e similaridade de cosseno.
* Adicione mais categorias em `CATEGORIES` se necessário para melhorar a sugestão.

---

## ✅ Teste rápido

1. Abra o navegador em `http://127.0.0.1:8000`
2. Verifique a rota raiz.
3. Teste as rotas `/tickets` e `/categories`.
4. Confira a categorização automática dos tickets.
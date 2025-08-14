from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base, Ticket, Comment, Person
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import Counter

# Cria tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ticket Categorizer")

# Modelo leve MiniLM
model = SentenceTransformer("all-MiniLM-L6-v2")

# Categorias em inglês
CATEGORIES = [
    "Login",
    "Returns",
    "Orders",
    "Payments / Promos / Invoices / Credits",
    "Damaged Product / Defect",
    "System Error / Bug",
    "Profile / Address",
    "Delivery",
    "Other",
]

category_embeddings = model.encode(CATEGORIES)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Ticket categorizer API running"}


@app.get("/tickets")
def list_tickets(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    results = []

    for t in tickets:
        # Concatenar subject + comentários
        text = t.subject + " " + " ".join([c.body for c in t.comments])
        ticket_embedding = model.encode([text])[0]

        # Similaridade com categorias
        sims = cosine_similarity([ticket_embedding], category_embeddings)[0]
        best_idx = np.argmax(sims)
        suggested_category = CATEGORIES[best_idx]

        results.append(
            {
                "ticket_id": t.id,
                "subject": t.subject,
                "suggested_category": suggested_category,
            }
        )

    return results


@app.get("/tickets/{ticket_id}")
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    text = ticket.subject + " " + " ".join([c.body for c in ticket.comments])
    ticket_embedding = model.encode([text])[0]

    # Similaridade com categorias
    sims = cosine_similarity([ticket_embedding], category_embeddings)[0]
    best_idx = np.argmax(sims)
    suggested_category = CATEGORIES[best_idx]

    return {
        "ticket_id": ticket.id,
        "subject": ticket.subject,
        "comments": [c.body for c in ticket.comments],
        "suggested_category": suggested_category,
    }


@app.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    category_counts = Counter()

    for t in tickets:
        # Concatenar subject + comentários
        text = t.subject + " " + " ".join([c.body for c in t.comments])
        ticket_embedding = model.encode([text])[0]

        # Similaridade com categorias
        sims = cosine_similarity([ticket_embedding], category_embeddings)[0]
        best_idx = np.argmax(sims)
        suggested_category = CATEGORIES[best_idx]

        # Incrementa contador
        category_counts[suggested_category] += 1

    # Converte para lista de dicts
    results = [{"category": cat, "count": count} for cat, count in category_counts.items()]
    return results
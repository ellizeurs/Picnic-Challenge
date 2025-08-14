import json
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from .models import Base, Person, Ticket, Comment, Attachment, Role
from .database import engine, SessionLocal

# Create tables
Base.metadata.create_all(bind=engine)

def get_or_create_person(session: Session, name: str, role: Role, email: str = None):
    query = session.query(Person).filter_by(role=role)
    if email:
        query = query.filter_by(email=email)
    else:
        query = query.filter_by(name=name)
    person = query.first()
    if not person:
        person = Person(name=name, role=role, email=email)
        session.add(person)
        session.flush() 
    return person

def import_tickets(json_path: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        tickets_data = json.load(f)


    db = SessionLocal()

    for t in tickets_data["tickets"]:
        # Create requester
        requester_data = t["requester"]
        requester = get_or_create_person(
            db,
            name=requester_data["name"],
            role=Role.requester,
            email=requester_data.get("email")
        )

        # Create ticket
        ticket = Ticket(
            subject=t["subject"],
            created_at=datetime.fromisoformat(t["created_at"].replace("Z", "+00:00")),
            requester=requester
        )
        db.add(ticket)
        db.flush()

        # Create comments
        for c in t.get("comments", []):
            author_data = c["author"]
            author = get_or_create_person(
                db,
                name=author_data["name"],
                role=Role(author_data["role"]),
                email=author_data.get("email")
            )

            comment = Comment(
                ticket=ticket,
                author=author,
                body=c["body"],
                public=c.get("public", True),
                created_at=datetime.fromisoformat(c["created_at"].replace("Z", "+00:00"))
            )
            db.add(comment)
            db.flush()

            # Create attachments
            for a in c.get("attachments", []):
                attachment = Attachment(
                    file_name=a["file_name"],
                    comment=comment
                )
                db.add(attachment)

    db.commit()
    db.close()

if __name__ == "__main__":
    import_tickets(Path("data/zendesk_mock_tickets_llm_flavor.json"))

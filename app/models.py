import enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Enum as SAEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Role(str, enum.Enum):
    requester = "requester"
    agent = "agent"

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # email agora é opcional
    email = Column(String, nullable=True, index=True)
    # role obrigatório, armazenado como string (native_enum=False funciona bem no SQLite)
    role = Column(SAEnum(Role, name="role_enum", native_enum=False), nullable=False)

    # Dica: manter unicidade por (email, role) quando email existir.
    # Para casos sem email, evitamos UNIQ por (name, role) na base (pode colidir),
    # e resolvemos na importação buscando por (name, role) quando email vier ausente.
    __table_args__ = (
        UniqueConstraint("email", "role", name="uq_people_email_role"),
    )

    tickets_requested = relationship(
        "Ticket", back_populates="requester", foreign_keys="Ticket.requester_id"
    )
    comments_authored = relationship(
        "Comment", back_populates="author", foreign_keys="Comment.author_id"
    )

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    requester_id = Column(Integer, ForeignKey("people.id"))
    requester = relationship("Person", back_populates="tickets_requested")

    comments = relationship("Comment", back_populates="ticket", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    body = Column(Text, nullable=False)
    public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    ticket = relationship("Ticket", back_populates="comments")
    author = relationship("Person", back_populates="comments_authored")
    attachments = relationship("Attachment", back_populates="comment", cascade="all, delete-orphan")

class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=False)

    comment = relationship("Comment", back_populates="attachments")

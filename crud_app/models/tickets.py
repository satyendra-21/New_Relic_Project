from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from crud_app.database import Base

class TicketDB(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String(50), unique=True, index=True)
    title = Column(String(255))
    description = Column(String(1000))
    priority = Column(String(50))
    status = Column(String(50))
class TicketCreate(BaseModel):
    title: str
    description: str
    priority: str


class TicketUpdate(BaseModel):
    title: str
    description: str
    priority: str
    status: str
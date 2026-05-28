from pydantic import BaseModel


class TicketCreate(BaseModel):
    title: str
    description: str
    priority: str


class TicketUpdate(BaseModel):
    title: str
    description: str
    priority: str
    status: str
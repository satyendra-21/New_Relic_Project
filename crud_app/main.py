import random
import uuid
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from crud_app.models.tickets import TicketCreate, TicketUpdate, TicketDB
from crud_app.utils.logger import logger
from crud_app.config import settings
from crud_app.database import get_db, engine, Base

app = FastAPI()

@app.on_event("startup")
def on_startup():
    print("Connecting to database and creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

@app.get("/")
def home():
    return {"message": "CRUD app is running with MySQL"}

@app.post("/tickets")
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    trace_id = str(uuid.uuid4())
    logger.info(
        f"traceId={trace_id} | "
        f"service=support-ticket-service | "
        f"event=ticket_creation_started"
    )

    total_tickets = db.query(TicketDB).count()
    ticket_id = f"INC-{total_tickets + 1}"

    db_ticket = TicketDB(
        ticket_id=ticket_id,
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        status="open"
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)

    logger.info(
        f"traceId={trace_id} | "
        f"service=support-ticket-service | "
        f"ticketId={ticket_id} | "
        f"event=ticket_created_successfully"
    )

    return db_ticket

@app.get("/tickets")
def get_all_tickets(db: Session = Depends(get_db)):
    return db.query(TicketDB).all()

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    trace_id = str(uuid.uuid4())
    logger.info(
        f"traceId={trace_id} | "
        f"service=support-ticket-service | "
        f"ticketId={ticket_id} | "
        f"event=ticket_fetch_started"
    )

    ticket = db.query(TicketDB).filter(TicketDB.ticket_id == ticket_id).first()
    if ticket:
        logger.info(
            f"traceId={trace_id} | "
            f"service=support-ticket-service | "
            f"ticketId={ticket_id} | "
            f"event=ticket_found"
        )
        return ticket

    logger.warning(
        f"traceId={trace_id} | "
        f"service=support-ticket-service | "
        f"ticketId={ticket_id} | "
        f"event=ticket_not_found"
    )
    raise HTTPException(status_code=404, detail="Ticket not found")

@app.put("/tickets/{ticket_id}")
def update_ticket(ticket_id: str, updated_ticket: TicketUpdate, db: Session = Depends(get_db)):
    trace_id = str(uuid.uuid4())
    logger.info(
        f"traceId={trace_id} | "
        f"service=support-ticket-service | "
        f"ticketId={ticket_id} | "
        f"event=ticket_update_started"
    )

    ticket = db.query(TicketDB).filter(TicketDB.ticket_id == ticket_id).first()
    if ticket:
        old_status = ticket.status

        ticket.title = updated_ticket.title
        ticket.description = updated_ticket.description
        ticket.priority = updated_ticket.priority
        ticket.status = updated_ticket.status

        db.commit()
        db.refresh(ticket)

        logger.info(
            f"traceId={trace_id} | "
            f"service=support-ticket-service | "
            f"ticketId={ticket_id} | "
            f"oldStatus={old_status} | "
            f"newStatus={updated_ticket.status} | "
            f"event=ticket_updated_successfully"
        )
        return {
            "message": "Ticket updated successfully",
            "status": "success",
            "data": ticket
        }

    logger.warning(
        f"traceId={trace_id} | "
        f"service=support-ticket-service | "
        f"ticketId={ticket_id} | "
        f"event=ticket_update_failed_ticket_not_found"
    )
    raise HTTPException(status_code=404, detail="Ticket not found")

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: str, db: Session = Depends(get_db)):
    trace_id = str(uuid.uuid4())
    logger.info(
        f"traceId={trace_id} | "
        f"service=support-ticket-service | "
        f"ticketId={ticket_id} | "
        f"event=ticket_delete_started"
    )

    ticket = db.query(TicketDB).filter(TicketDB.ticket_id == ticket_id).first()
    if ticket:
        db.delete(ticket)
        db.commit()

        logger.info(
            f"traceId={trace_id} | "
            f"service=support-ticket-service | "
            f"ticketId={ticket_id} | "
            f"event=ticket_deleted_successfully"
        )
        return {"message": f"Ticket {ticket_id} deleted successfully"}

    logger.warning(
        f"traceId={trace_id} | "
        f"service=support-ticket-service | "
        f"ticketId={ticket_id} | "
        f"event=ticket_delete_failed_ticket_not_found"
    )
    raise HTTPException(status_code=404, detail="Ticket not found")

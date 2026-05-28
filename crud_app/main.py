import random
import uuid
from fastapi import FastAPI, HTTPException
from crud_app.models.tickets import TicketCreate, TicketUpdate
from crud_app.utils.logger import logger

app = FastAPI()

tickets = []


@app.get("/")
def home():
    return {"message": "CRUD app is running"}


@app.post("/tickets")
@app.post("/tickets")
def create_ticket(ticket: TicketCreate):

    trace_id = str(uuid.uuid4())

    logger.info(
        f"traceId={trace_id} | "
        f"service=support-ticket-service | "
        f"event=ticket_creation_started"
    )

    ticket_data = {
        "ticket_id": f"INC-{len(tickets)+1}",
        "title": ticket.title,
        "description": ticket.description,
        "priority": ticket.priority,
        "status": "open"
    }

    tickets.append(ticket_data)

    logger.info(
        f"traceId={trace_id} | "
        f"service=support-ticket-service | "
        f"ticketId={ticket_data['ticket_id']} | "
        f"event=ticket_created_successfully"
    )

    return ticket_data
@app.get("/tickets")
def get_all_tickets():
    return tickets
@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):

    trace_id = str(uuid.uuid4())

    logger.info(
        f"traceId={trace_id} | "
        f"service=support-ticket-service | "
        f"ticketId={ticket_id} | "
        f"event=ticket_fetch_started"
    )

    for ticket in tickets:

        if ticket["ticket_id"] == ticket_id:

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

    return {"error": "Ticket not found"}
@app.put("/tickets/{ticket_id}")
def update_ticket(ticket_id: str, updated_ticket: TicketUpdate):

    trace_id = str(uuid.uuid4())

    logger.info(
        f"traceId={trace_id} | "
        f"service=support-ticket-service | "
        f"ticketId={ticket_id} | "
        f"event=ticket_update_started"
    )

    for ticket in tickets:

        if ticket["ticket_id"] == ticket_id:
            simulate_failure = random.choice([True, False])

            if simulate_failure:

                logger.error(
                    f"traceId={trace_id} | "
                    f"service=support-ticket-service | "
                    f"ticketId={ticket_id} | "
                    f"event=database_timeout | "
                    f"message=Failed to update ticket"
                )

                raise HTTPException(
    status_code=500,
    detail="Database timeout occurred while updating ticket"
)
            old_status = ticket["status"]

            ticket["title"] = updated_ticket.title
            ticket["description"] = updated_ticket.description
            ticket["priority"] = updated_ticket.priority
            ticket["status"] = updated_ticket.status

            logger.info(
                f"traceId={trace_id} | "
                f"service=support-ticket-service | "
                f"ticketId={ticket_id} | "
                f"oldStatus={old_status} | "
                f"newStatus={updated_ticket.status} | "
                f"event=ticket_updated_successfully"
            )

            return ticket

    logger.warning(
        f"traceId={trace_id} | "
        f"service=support-ticket-service | "
        f"ticketId={ticket_id} | "
        f"event=ticket_update_failed_ticket_not_found"
    )

    return {"error": "Ticket not found"}
@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: str):

    trace_id = str(uuid.uuid4())

    logger.info(
        f"traceId={trace_id} | "
        f"service=support-ticket-service | "
        f"ticketId={ticket_id} | "
        f"event=ticket_delete_started"
    )

    for ticket in tickets:

        if ticket["ticket_id"] == ticket_id:

            tickets.remove(ticket)

            logger.info(
                f"traceId={trace_id} | "
                f"service=support-ticket-service | "
                f"ticketId={ticket_id} | "
                f"event=ticket_deleted_successfully"
            )

            return {
                "message": f"Ticket {ticket_id} deleted successfully"
            }

    logger.warning(
        f"traceId={trace_id} | "
        f"service=support-ticket-service | "
        f"ticketId={ticket_id} | "
        f"event=ticket_delete_failed_ticket_not_found"
    )

    return {"error": "Ticket not found"}
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from uuid import uuid4

# Anonymous ticket status options
class TicketStatus(str):
    NEW = "new"
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

# PUBLIC_INTERFACE
class TicketCreateRequest(BaseModel):
    """Model for creating a new anonymous support ticket."""
    subject: str = Field(..., description="Short title or subject of the ticket")
    content: str = Field(..., description="Details about the issue or request")

# PUBLIC_INTERFACE
class TicketResponse(BaseModel):
    """Model for representing a ticket. No user info stored."""
    ticket_id: str
    subject: str
    content: str
    status: str

# Anonymous ticket repository (in-memory for demonstration; swap with persistent db as needed)
class TicketRepository:
    def __init__(self):
        self._tickets: Dict[str, Dict] = {}

    # PUBLIC_INTERFACE
    def create_ticket(self, subject: str, content: str) -> Dict:
        ticket_id = str(uuid4())
        ticket = {
            "ticket_id": ticket_id,
            "subject": subject,
            "content": content,
            "status": TicketStatus.NEW,
        }
        self._tickets[ticket_id] = ticket
        return ticket

    # PUBLIC_INTERFACE
    def get_ticket(self, ticket_id: str) -> Optional[Dict]:
        return self._tickets.get(ticket_id)

    # PUBLIC_INTERFACE
    def update_status(self, ticket_id: str, new_status: str) -> Optional[Dict]:
        ticket = self._tickets.get(ticket_id)
        if ticket and new_status in (TicketStatus.NEW, TicketStatus.OPEN, TicketStatus.IN_PROGRESS, TicketStatus.CLOSED):
            ticket["status"] = new_status
            return ticket
        return None

    # PUBLIC_INTERFACE
    def list_tickets(self) -> List[Dict]:
        return list(self._tickets.values())

# Single shared repository instance (thread-unsafe; for demo/dev only)
ticket_repo = TicketRepository()

router = APIRouter()

# PUBLIC_INTERFACE
@router.post(
    "/tickets/",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new anonymous support ticket",
    tags=["tickets"],
)
async def create_ticket(request: TicketCreateRequest):
    """
    Submit a new support ticket anonymously.
    """
    ticket = ticket_repo.create_ticket(request.subject, request.content)
    return ticket

# PUBLIC_INTERFACE
@router.get(
    "/tickets/{ticket_id}",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK,
    summary="Get ticket details by ID",
    tags=["tickets"],
)
async def get_ticket(ticket_id: str):
    """
    Retrieve the status and details of a specific ticket by its ID.
    """
    ticket = ticket_repo.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

# PUBLIC_INTERFACE
class StatusUpdateRequest(BaseModel):
    """Request model for updating a ticket's status."""
    status: str = Field(..., description="New status (new, open, in_progress, closed)")

@router.patch(
    "/tickets/{ticket_id}/status",
    response_model=TicketResponse,
    summary="Update the status of a specific ticket",
    tags=["tickets"]
)
async def update_ticket_status(ticket_id: str, req: StatusUpdateRequest):
    """
    Update the status of a support ticket by its ID.
    """
    ticket = ticket_repo.update_status(ticket_id, req.status)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found or invalid status")
    return ticket

# PUBLIC_INTERFACE
@router.get(
    "/tickets/",
    response_model=List[TicketResponse],
    summary="List all tickets (anonymously)",
    tags=["tickets"]
)
async def list_tickets():
    """
    Retrieve all tickets in the system (anonymous—no user association).
    """
    return ticket_repo.list_tickets()

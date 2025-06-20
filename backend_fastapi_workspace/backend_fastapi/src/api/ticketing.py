from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from uuid import uuid4
import os
import json
import threading

TICKETS_FILE = os.path.join(os.path.dirname(__file__), '../../tickets.json')
TICKETS_FILE = os.path.abspath(TICKETS_FILE)

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

class StatusUpdateRequest(BaseModel):
    """Request model for updating a ticket's status."""
    status: str = Field(..., description="New status (new, open, in_progress, closed)")

def _thread_safe_file_lock():
    """Simple single-process file lock using threading.RLock for critical file sections"""
    return threading.RLock()

# Anonymous ticket repository with JSON file persistence
class TicketRepository:
    def __init__(self, json_path=TICKETS_FILE):
        self._json_path = json_path
        # A re-entrant lock is used to ensure file consistency per process
        self._lock = _thread_safe_file_lock()
        self._tickets: Dict[str, Dict] = {}
        self._load()

    def _load(self):
        """Load tickets from the JSON file, or initialize empty if not present."""
        with self._lock:
            if not os.path.isfile(self._json_path):
                self._tickets = {}
                return
            try:
                with open(self._json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Ensure structure is dict
                if isinstance(data, dict):
                    self._tickets = data
                else:
                    self._tickets = {}
            except Exception:
                self._tickets = {}

    def _save(self):
        """Persist the tickets dictionary to the file atomically (thread-safe for one process)."""
        with self._lock:
            tmp_path = self._json_path + ".tmp"
            try:
                with open(tmp_path, 'w', encoding='utf-8') as f:
                    json.dump(self._tickets, f, ensure_ascii=False, indent=2)
                os.replace(tmp_path, self._json_path)
            except Exception:
                pass  # In production, log/write error

    # PUBLIC_INTERFACE
    def create_ticket(self, subject: str, content: str) -> Dict:
        """Create a new ticket and persist to file."""
        with self._lock:
            ticket_id = str(uuid4())
            ticket = {
                "ticket_id": ticket_id,
                "subject": subject,
                "content": content,
                "status": TicketStatus.NEW,
            }
            self._tickets[ticket_id] = ticket
            self._save()
            return ticket

    # PUBLIC_INTERFACE
    def get_ticket(self, ticket_id: str) -> Optional[Dict]:
        """Get a ticket by its ID."""
        with self._lock:
            return self._tickets.get(ticket_id)

    # PUBLIC_INTERFACE
    def update_status(self, ticket_id: str, new_status: str) -> Optional[Dict]:
        """Update the status of a ticket and persist to file."""
        with self._lock:
            ticket = self._tickets.get(ticket_id)
            if (
                ticket
                and new_status
                in (TicketStatus.NEW, TicketStatus.OPEN, TicketStatus.IN_PROGRESS, TicketStatus.CLOSED)
            ):
                ticket["status"] = new_status
                self._save()
                return ticket
            return None

    # PUBLIC_INTERFACE
    def list_tickets(self) -> List[Dict]:
        """List all tickets."""
        with self._lock:
            return list(self._tickets.values())

    # PUBLIC_INTERFACE
    def reload_from_file(self):
        """Reload tickets from the JSON file. Not typically needed outside app startup/test."""
        self._load()

# Single shared repository instance (thread/threadsafe across endpoints for demo/dev use)
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

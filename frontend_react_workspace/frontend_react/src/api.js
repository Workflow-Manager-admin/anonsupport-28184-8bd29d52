 /**
 * API helper for anonymous ticketing system.
 * All routes and payloads follow the backend OpenAPI (FastAPI).
 */

const BASE_URL = 'https://vscode-internal-90-qa.qa01.cloud.kavia.ai:3001/tickets/';

/**
 * List all accessible tickets.
 * PUBLIC_INTERFACE
 */
export async function listTickets() {
  const res = await fetch(BASE_URL, {
    method: 'GET',
    headers: { 'Accept': 'application/json' },
  });
  if (!res.ok) throw new Error('Failed to fetch tickets');
  return res.json();
}

/**
 * Create a new anonymous ticket.
 * fields = { subject, content }
 * PUBLIC_INTERFACE
 */
export async function createTicket(fields) {
  const res = await fetch(BASE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    body: JSON.stringify(fields),
  });
  if (res.status === 422) {
    throw new Error("Missing or invalid info.");
  }
  if (!res.ok) throw new Error('Failed to submit ticket');
  return res.json();
}

/**
 * Get ticket status/details by ticket_id.
 * PUBLIC_INTERFACE
 */
export async function getTicket(ticket_id) {
  const res = await fetch(`${BASE_URL}${encodeURIComponent(ticket_id)}`, {
    method: 'GET',
    headers: { 'Accept': 'application/json' },
  });
  if (!res.ok) throw new Error('Ticket not found');
  return res.json();
}

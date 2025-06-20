import React from 'react';

/**
 * List of Tickets (anonymous, modern minimal)
 * Shows subject, content/snippet, status, and ticket ID.
 * PUBLIC_INTERFACE
 */
function TicketList({ tickets, loading }) {
  return (
    <div className="ticket-list">
      <div className="ticket-list-title">Your Tickets</div>
      {loading && <div>Loading tickets…</div>}
      {!loading && (!tickets || tickets.length === 0) && (
        <div style={{color:"#7b7b7b",margin:"12px 0"}}>No tickets found. Submit your first ticket above!</div>
      )}
      {!loading && tickets && tickets.map((ticket) =>
        <div className="ticket-row" key={ticket.ticket_id}>
          <div className="ticket-subject">{ticket.subject}</div>
          <div className="ticket-meta">
            Ticket ID: <code>{ticket.ticket_id}</code>
            <span className="ticket-status">({ticket.status})</span>
          </div>
          <div style={{fontSize:".97rem",color:"#444",marginTop:"2px"}}>
            {ticket.content?.length > 120 ?
              ticket.content.slice(0,110) + '…' :
              ticket.content}
          </div>
        </div>
      )}
    </div>
  );
}

export default TicketList;

import React, { useState } from 'react';

/**
 * List of Tickets (anonymous, modern minimal)
 * Shows subject, content/snippet, status, and ticket ID, with edit/delete actions.
 * PUBLIC_INTERFACE
 */
function TicketList({ tickets, loading, onEdit, onDelete }) {
  // Local state for managing what ticket is currently being edited and edit fields.
  const [editingTicketId, setEditingTicketId] = useState(null);
  const [editFields, setEditFields] = useState({ subject: '', content: '' });
  const [editLoading, setEditLoading] = useState(false);

  // Start editing a ticket
  function startEdit(ticket) {
    setEditingTicketId(ticket.ticket_id);
    setEditFields({ subject: ticket.subject, content: ticket.content });
  }

  // Handle changes in the edit form
  function handleEditChange(e) {
    setEditFields((fields) => ({
      ...fields, [e.target.name]: e.target.value
    }));
  }

  // Handle confirm edit (calls parent callback)
  async function handleSaveEdit(ticket_id) {
    if (!editFields.subject.trim() || !editFields.content.trim()) return;
    setEditLoading(true);
    await onEdit(ticket_id, { subject: editFields.subject.trim(), content: editFields.content.trim() });
    setEditLoading(false);
    setEditingTicketId(null);
  }

  function handleCancelEdit() {
    setEditingTicketId(null);
  }

  return (
    <div className="ticket-list">
      <div className="ticket-list-title">Your Tickets</div>
      {loading && <div>Loading tickets…</div>}
      {!loading && (!tickets || tickets.length === 0) && (
        <div style={{color:"#7b7b7b",margin:"12px 0"}}>No tickets found. Submit your first ticket above!</div>
      )}
      {!loading && tickets && tickets.map((ticket) =>
        <div className="ticket-row" key={ticket.ticket_id}>
          {editingTicketId === ticket.ticket_id ? (
            <form
              onSubmit={e => {
                e.preventDefault();
                handleSaveEdit(ticket.ticket_id);
              }}
              style={{display:'flex',flexDirection:'column',gap:8}}
            >
              <input
                name="subject"
                className="ticket-edit-input"
                value={editFields.subject}
                onChange={handleEditChange}
                maxLength={70}
                disabled={editLoading}
                style={{marginBottom:6}}
                required
              />
              <textarea
                name="content"
                className="ticket-edit-input"
                value={editFields.content}
                onChange={handleEditChange}
                maxLength={700}
                disabled={editLoading}
                required
                style={{minHeight:46,marginBottom:6}}
              />
              <div style={{display:'flex',gap:6,marginTop:2}}>
                <button className="btn" type="submit" disabled={editLoading}>
                  {editLoading ? 'Saving…' : 'Save'}
                </button>
                <button className="btn" type="button" onClick={handleCancelEdit} disabled={editLoading}>
                  Cancel
                </button>
              </div>
            </form>
          ) : (
            <>
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
              <div style={{marginTop:8,display:'flex',gap:8}}>
                <button
                  className="btn"
                  onClick={() => startEdit(ticket)}
                  style={{backgroundColor: "var(--accent)"}}
                  type="button"
                >Edit</button>
                <button
                  className="btn"
                  onClick={() => onDelete(ticket.ticket_id)}
                  style={{backgroundColor: "var(--error)"}}
                  type="button"
                >Delete</button>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default TicketList;

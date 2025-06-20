import React, { useEffect, useState } from 'react';
import './App.css';
import TicketForm from './TicketForm';
import TicketList from './TicketList';
import { listTickets, createTicket } from './api';

// PUBLIC_INTERFACE
function App() {
  // State for list of tickets and loading/error
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [notification, setNotification] = useState(null);

  // Fetch tickets on mount
  useEffect(() => {
    fetchTickets();
  }, []);

  // Fetch all tickets (anonymous)
  async function fetchTickets() {
    setLoading(true);
    try {
      const data = await listTickets();
      setTickets(data);
    } catch (err) {
      setNotification({ message: 'Failed to load tickets.', type: 'error' });
    } finally {
      setLoading(false);
    }
  }

  // Handle new ticket submission (refresh list after)
  const handleTicketSubmit = async (fields, clearForm) => {
    try {
      await createTicket(fields);
      setNotification({ message: 'Ticket submitted!', type: 'success' });
      clearForm();
      fetchTickets();
    } catch (err) {
      setNotification({ message: err.message || 'Submit failed', type: 'error' });
    }
  };

  // Hide notification after 3s
  useEffect(() => {
    if (notification) {
      const to = setTimeout(() => setNotification(null), 3000);
      return () => clearTimeout(to);
    }
  }, [notification]);

  return (
    <div className="app">
      <nav className="navbar">
        <div className="header-container">
          <div className="logo">
            <span className="logo-symbol">*</span> AnonSupport
          </div>
          <span style={{fontWeight:400,fontSize:"1.03rem"}}>Anonymous Ticketing</span>
        </div>
      </nav>

      <main>
        <div className="container" style={{marginTop: "28px"}}>
          <TicketForm onSubmit={handleTicketSubmit} />
          <TicketList tickets={tickets} loading={loading} />
        </div>
      </main>

      <footer className="footer">
        <span>AnonSupport &copy; {new Date().getFullYear()} – Anonymous ticketing platform.</span>
      </footer>

      {notification && (
        <div className={`toast toast-${notification.type}`}>
          {notification.message}
        </div>
      )}
    </div>
  );
}

export default App;

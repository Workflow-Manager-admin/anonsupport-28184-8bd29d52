import React, { useState } from 'react';

/**
 * Anonymous Ticket Submission Form
 * Minimal, modern; calls onSubmit(subject, content) on submit.
 * PUBLIC_INTERFACE
 */
function TicketForm({ onSubmit }) {
  const [subject, setSubject] = useState('');
  const [content, setContent] = useState('');
  const [submitting, setSubmitting] = useState(false);

  // Reset the form fields
  function clearForm() {
    setSubject('');
    setContent('');
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!subject.trim() || !content.trim()) return;
    setSubmitting(true);
    await onSubmit({ subject: subject.trim(), content: content.trim() }, clearForm);
    setSubmitting(false);
  };

  return (
    <form className="ticket-form" onSubmit={handleSubmit} autoComplete="off">
      <label>Subject</label>
      <input
        data-testid="subject"
        value={subject}
        onChange={(e) => setSubject(e.target.value)}
        placeholder="Short summary"
        maxLength={70}
        required
        disabled={submitting}
      />
      <label>Details</label>
      <textarea
        data-testid="content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Describe your issue/request…"
        maxLength={700}
        required
        disabled={submitting}
      />
      <button className="btn btn-large" type="submit" disabled={submitting || !subject || !content}>
        {submitting ? 'Submitting...' : 'Submit Ticket'}
      </button>
    </form>
  );
}

export default TicketForm;

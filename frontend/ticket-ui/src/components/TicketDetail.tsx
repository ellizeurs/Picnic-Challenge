import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../api";

interface Ticket {
  ticket_id: number;
  subject: string;
  comments: string[];
  suggested_category: string;
}

export const TicketDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [ticket, setTicket] = useState<Ticket | null>(null);

  useEffect(() => {
    api.get<Ticket>(`/tickets/${id}`)
      .then(res => setTicket(res.data))
      .catch(err => console.error(err));
  }, [id]);

  if (!ticket) return <p>Loading...</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h2>{ticket.subject}</h2>
      <p><strong>Category:</strong> {ticket.suggested_category}</p>
      <h3>Comments</h3>
      <ul>
        {ticket.comments.map((c, i) => (
          <li key={i}>{c}</li>
        ))}
      </ul>
      <Link to="/">← Back to Dashboard</Link>
    </div>
  );
};

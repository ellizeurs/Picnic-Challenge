import React, { useEffect, useState } from "react";
import { api } from "../api";
import { Link } from "react-router-dom";

interface Ticket {
  ticket_id: number;
  subject: string;
  suggested_category: string;
}

export const TicketsList: React.FC = () => {
  const [tickets, setTickets] = useState<Ticket[]>([]);

  useEffect(() => {
    api.get<Ticket[]>("/tickets")
      .then(res => setTickets(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h2>Tickets</h2>
      <ul>
        {tickets.map(ticket => (
          <li key={ticket.ticket_id}>
            <Link to={`/ticket/${ticket.ticket_id}`}>
              <strong>{ticket.subject}</strong>
            </Link>{" "}
            — <em>{ticket.suggested_category}</em>
          </li>
        ))}
      </ul>
    </div>
  );
};

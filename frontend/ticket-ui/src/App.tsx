import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { TicketsList } from "./components/TicketsList";
import { CategoriesList } from "./components/CategoriesList";
import { TicketDetail } from "./components/TicketDetail";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <div style={{ padding: "20px" }}>
            <h1>Ticket Categorizer Dashboard</h1>
            <CategoriesList />
            <TicketsList />
          </div>
        } />
        <Route path="/ticket/:id" element={<TicketDetail />} />
      </Routes>
    </Router>
  );
}

export default App;

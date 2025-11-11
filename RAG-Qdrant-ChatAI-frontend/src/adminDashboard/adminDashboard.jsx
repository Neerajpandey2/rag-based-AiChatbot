import React from "react";
import { Outlet, useNavigate } from "react-router-dom";
import "./adminDashboard.css";

export default function AdminDashboard() {
  const navigate = useNavigate();

  return (
    <div className="admin-dashboard">
      {/* Sidebar */}
      <aside className="sidebar">
        <h2 className="sidebar-title">Admin Panel</h2>
        <nav className="nav-buttons">
          <button onClick={() => navigate("documentUpload")}>
            📂 Upload Document
          </button>
          <button onClick={() => navigate("getAllQa")}>
            ❓ Get All QA
          </button>
          <button className="back-btn" onClick={() => navigate(-1)}>
            ⬅ Go Back
          </button>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="content">
        <h1 className="dashboard-heading">Admin Dashboard</h1>
        <div className="child-pages">
          <Outlet />
        </div>
      </main>
    </div>
  );
}

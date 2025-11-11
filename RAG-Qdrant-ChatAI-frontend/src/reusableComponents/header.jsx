import { Link } from "react-router-dom";
import "./header.css";

function Header() {
  return (
    <header className="header">
      <div className="logo">🤖 My Chatbot</div>
      <nav>
        <ul className="nav-links">
          <li><Link to="/">Chatbot</Link></li>
          <li><Link to="/about">About</Link></li>
          <li><Link to="/contact">Contact</Link></li>
          <li><Link to="/admin">Admin</Link></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;

import { Link } from "react-router-dom";
import { useUser } from "../context/UserContext";
import Logo from "./Logo";

function Navbar() {
  const { currentUser, logout } = useUser();

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        <Logo />
      </Link>

      <div className="navbar-links">
        {currentUser ? (
          <>
            <Link to="/bookings">My Bookings</Link>
            {currentUser.role === "ADMIN" && <Link to="/admin">Admin</Link>}
            <span className="navbar-user">Hi, {currentUser.name}</span>
            <button className="btn btn-outline" onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/register">Register</Link>
            <Link to="/login">Login</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;

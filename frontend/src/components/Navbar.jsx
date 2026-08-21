import { Link } from "react-router-dom";
import { useUser } from "../context/UserContext";

function Navbar() {
  const { currentUser, logout } = useUser();

  return (
    <nav className="navbar">
      <Link to="/">FleetX</Link>
      <Link to="/register">Register</Link>

      {currentUser ? (
        <>
          <Link to="/bookings">My Bookings</Link>
          {currentUser.role === "ADMIN" && <Link to="/admin">Admin</Link>}
          <span>Hi, {currentUser.name}</span>
          <button className="btn" onClick={logout}>Logout</button>
        </>
      ) : (
        <Link to="/login">Login</Link>
      )}
    </nav>
  );
}

export default Navbar;

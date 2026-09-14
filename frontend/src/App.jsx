import "./App.css";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import HomePage from "./pages/HomePage";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import MyBookingsPage from "./pages/MyBookingsPage";
import AdminPage from "./pages/AdminPage";

function App() {
  return (
    <div className="page">
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/register" element={<div className="page-inner"><RegisterPage /></div>} />
        <Route path="/login" element={<div className="page-inner"><LoginPage /></div>} />
        <Route path="/bookings" element={<div className="page-inner"><MyBookingsPage /></div>} />
        <Route path="/admin" element={<div className="page-inner"><AdminPage /></div>} />
      </Routes>
    </div>
  );
}

export default App;

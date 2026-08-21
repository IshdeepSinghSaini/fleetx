import { useState, useEffect } from "react";
import axios from "axios";
import { useUser } from "../context/UserContext";

function AdminPage() {
  const { currentUser } = useUser();
  const [vehicles, setVehicles] = useState([]);
  const [bookings, setBookings] = useState([]);

  const [name, setName] = useState("");
  const [type, setType] = useState("");
  const [numberPlate, setNumberPlate] = useState("");
  const [pricePerDay, setPricePerDay] = useState("");
  const [seats, setSeats] = useState("");
  const [location, setLocation] = useState("");

  const fetchVehicles = () => {
    axios.get("http://localhost:8080/api/vehicles").then((res) => setVehicles(res.data));
  };

  const fetchBookings = () => {
    axios.get("http://localhost:8080/api/bookings").then((res) => setBookings(res.data));
  };

  useEffect(() => {
    fetchVehicles();
    fetchBookings();
  }, []);

  const handleAddVehicle = (e) => {
    e.preventDefault();
    axios.post("http://localhost:8080/api/vehicles", {
      name,
      type,
      numberPlate,
      pricePerDay: Number(pricePerDay),
      seats: Number(seats),
      location,
    }).then(() => {
      setName("");
      setType("");
      setNumberPlate("");
      setPricePerDay("");
      setSeats("");
      setLocation("");
      fetchVehicles();
    });
  };

  const handleDeleteVehicle = (id) => {
    axios.delete(`http://localhost:8080/api/vehicles/${id}`)
      .then(fetchVehicles)
      .catch((error) => {
        alert(error.response?.data?.message || "Failed to delete vehicle.");
      });
  };

  if (!currentUser || currentUser.role !== "ADMIN") {
    return <p>Access denied. Admins only.</p>;
  }

  return (
    <div>
      <h2>Admin Dashboard</h2>

      <div className="card">
        <h3>Add Vehicle</h3>
        <form onSubmit={handleAddVehicle} className="form-group">
          <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
          <input placeholder="Type (CAR/BIKE/SUV)" value={type} onChange={(e) => setType(e.target.value)} />
          <input placeholder="Number Plate" value={numberPlate} onChange={(e) => setNumberPlate(e.target.value)} />
          <input placeholder="Price per day" value={pricePerDay} onChange={(e) => setPricePerDay(e.target.value)} />
          <input placeholder="Seats" value={seats} onChange={(e) => setSeats(e.target.value)} />
          <input placeholder="Location" value={location} onChange={(e) => setLocation(e.target.value)} />
          <button type="submit" className="btn">Add Vehicle</button>
        </form>
      </div>

      <div className="card">
        <h3>All Vehicles</h3>
        {vehicles.map((v) => (
          <div key={v.id} style={{ marginBottom: 10 }}>
            <p>{v.name} — {v.type} — ₹{v.pricePerDay}/day — {v.status}</p>
            <button className="btn" onClick={() => handleDeleteVehicle(v.id)}>Delete</button>
          </div>
        ))}
      </div>

      <div className="card">
        <h3>All Bookings</h3>
        {bookings.map((b) => (
          <div key={b.id} style={{ marginBottom: 10 }}>
            <p>
              {b.user.name} booked {b.vehicle.name} ({b.startDate} to {b.endDate}) — {b.status}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AdminPage;

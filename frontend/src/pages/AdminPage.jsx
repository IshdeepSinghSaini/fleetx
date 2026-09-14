import { useState, useEffect } from "react";
import axios from "axios";
import { useUser } from "../context/UserContext";

function AdminPage() {
  const { currentUser } = useUser();
  const [vehicles, setVehicles] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [payments, setPayments] = useState([]);
  const [users, setUsers] = useState([]);
  const [maintenanceLogs, setMaintenanceLogs] = useState([]);

  const [name, setName] = useState("");
  const [type, setType] = useState("");
  const [numberPlate, setNumberPlate] = useState("");
  const [pricePerDay, setPricePerDay] = useState("");
  const [seats, setSeats] = useState("");
  const [location, setLocation] = useState("");
  const [imageUrl, setImageUrl] = useState("");

  const [maintVehicleId, setMaintVehicleId] = useState("");
  const [maintDescription, setMaintDescription] = useState("");
  const [maintCost, setMaintCost] = useState("");
  const [maintStartDate, setMaintStartDate] = useState("");

  const fetchVehicles = () => {
    axios.get("http://localhost:8080/api/vehicles").then((res) => setVehicles(res.data));
  };

  const fetchBookings = () => {
    axios.get("http://localhost:8080/api/bookings").then((res) => setBookings(res.data));
  };

  const fetchPayments = () => {
    axios.get("http://localhost:8080/api/payments").then((res) => setPayments(res.data));
  };

  const fetchUsers = () => {
    axios.get("http://localhost:8080/api/users").then((res) => setUsers(res.data));
  };

  const fetchMaintenanceLogs = () => {
    axios.get("http://localhost:8080/api/maintenance").then((res) => setMaintenanceLogs(res.data));
  };

  useEffect(() => {
    fetchVehicles();
    fetchBookings();
    fetchPayments();
    fetchUsers();
    fetchMaintenanceLogs();
  }, []);

  const totalRevenue = payments
    .filter((p) => p.status === "SUCCESS")
    .reduce((sum, p) => sum + p.amount, 0);

  const availableCount = vehicles.filter((v) => v.status === "AVAILABLE").length;
  const activeBookings = bookings.filter((b) => b.status === "ACTIVE").length;

  const handleAddVehicle = (e) => {
    e.preventDefault();
    axios.post("http://localhost:8080/api/vehicles", {
      name,
      type,
      numberPlate,
      pricePerDay: Number(pricePerDay),
      seats: Number(seats),
      location,
      imageUrl,
    }).then(() => {
      setName("");
      setType("");
      setNumberPlate("");
      setPricePerDay("");
      setSeats("");
      setLocation("");
      setImageUrl("");
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

  const handleStartMaintenance = (e) => {
    e.preventDefault();
    axios.post(`http://localhost:8080/api/maintenance/vehicle/${maintVehicleId}`, {
      description: maintDescription,
      cost: Number(maintCost),
      startDate: maintStartDate,
    }).then(() => {
      setMaintVehicleId("");
      setMaintDescription("");
      setMaintCost("");
      setMaintStartDate("");
      fetchVehicles();
      fetchMaintenanceLogs();
    }).catch((error) => {
      alert(error.response?.data?.message || "Failed to start maintenance.");
    });
  };

  const handleCompleteMaintenance = (id) => {
    axios.put(`http://localhost:8080/api/maintenance/${id}/complete`)
      .then(() => {
        fetchVehicles();
        fetchMaintenanceLogs();
      });
  };

  const handleDeleteUser = (id) => {
    axios.delete(`http://localhost:8080/api/users/${id}`)
      .then(fetchUsers)
      .catch((error) => {
        alert(error.response?.data?.message || "Failed to delete user.");
      });
  };

  const handleRoleChange = (id, role) => {
    axios.put(`http://localhost:8080/api/users/${id}/role`, { role })
      .then(fetchUsers)
      .catch((error) => {
        alert(error.response?.data?.message || "Failed to update role.");
      });
  };

  if (!currentUser || currentUser.role !== "ADMIN") {
    return <p>Access denied. Admins only.</p>;
  }

  return (
    <div>
      <h2>Admin Dashboard</h2>

      <div className="stat-grid">
        <div className="stat-tile">
          <p className="stat-value">{vehicles.length}</p>
          <p className="stat-label">Total Vehicles</p>
        </div>
        <div className="stat-tile">
          <p className="stat-value">{availableCount}</p>
          <p className="stat-label">Available Now</p>
        </div>
        <div className="stat-tile">
          <p className="stat-value">{activeBookings}</p>
          <p className="stat-label">Active Bookings</p>
        </div>
        <div className="stat-tile">
          <p className="stat-value">₹{totalRevenue}</p>
          <p className="stat-label">Total Revenue</p>
        </div>
      </div>

      <div className="card">
        <h3>Add Vehicle</h3>
        <form onSubmit={handleAddVehicle} className="form-group">
          <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
          <select value={type} onChange={(e) => setType(e.target.value)}>
            <option value="">Select type</option>
            <option value="CAR">CAR</option>
            <option value="BIKE">BIKE</option>
          </select>
          <input placeholder="Number Plate" value={numberPlate} onChange={(e) => setNumberPlate(e.target.value)} />
          <input placeholder="Price per day" value={pricePerDay} onChange={(e) => setPricePerDay(e.target.value)} />
          <input placeholder="Seats" value={seats} onChange={(e) => setSeats(e.target.value)} />
          <input placeholder="Location" value={location} onChange={(e) => setLocation(e.target.value)} />
          <input placeholder="Image URL" value={imageUrl} onChange={(e) => setImageUrl(e.target.value)} />
          <button type="submit" className="btn">Add Vehicle</button>
        </form>
      </div>

      <div className="card">
        <h3>All Vehicles</h3>
        {vehicles.map((v) => (
          <div key={v.id} className="list-row">
            <div>
              <p style={{ margin: 0, fontWeight: 500 }}>{v.name}</p>
              <p style={{ margin: 0 }}>{v.type} — ₹{v.pricePerDay}/day — {v.status}</p>
            </div>
            <button className="btn btn-danger" onClick={() => handleDeleteVehicle(v.id)}>Delete</button>
          </div>
        ))}
      </div>

      <div className="card">
        <h3>Vehicle Maintenance</h3>
        <form onSubmit={handleStartMaintenance} className="form-group">
          <select value={maintVehicleId} onChange={(e) => setMaintVehicleId(e.target.value)}>
            <option value="">Select vehicle</option>
            {vehicles.filter((v) => v.status !== "MAINTENANCE").map((v) => (
              <option key={v.id} value={v.id}>{v.name}</option>
            ))}
          </select>
          <input placeholder="Description (e.g. Oil change)" value={maintDescription} onChange={(e) => setMaintDescription(e.target.value)} />
          <input placeholder="Cost" value={maintCost} onChange={(e) => setMaintCost(e.target.value)} />
          <input type="date" value={maintStartDate} onChange={(e) => setMaintStartDate(e.target.value)} />
          <button type="submit" className="btn">Start Maintenance</button>
        </form>

        <div style={{ marginTop: 16 }}>
          {maintenanceLogs.map((log) => (
            <div key={log.id} className="list-row">
              <div>
                <p style={{ margin: 0, fontWeight: 500 }}>
                  {log.vehicle.name} — {log.description}
                </p>
                <p style={{ margin: 0 }}>
                  ₹{log.cost} — From {log.startDate} {log.endDate ? `to ${log.endDate}` : "(ongoing)"}
                </p>
              </div>
              {!log.endDate && (
                <button className="btn" onClick={() => handleCompleteMaintenance(log.id)}>Mark Complete</button>
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <h3>Manage Users</h3>
        {users.map((u) => (
          <div key={u.id} className="list-row">
            <div>
              <p style={{ margin: 0, fontWeight: 500 }}>{u.name}</p>
              <p style={{ margin: 0 }}>{u.email}</p>
            </div>
            <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
              <select value={u.role} onChange={(e) => handleRoleChange(u.id, e.target.value)}>
                <option value="CUSTOMER">CUSTOMER</option>
                <option value="ADMIN">ADMIN</option>
              </select>
              <button className="btn btn-danger" onClick={() => handleDeleteUser(u.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <h3>All Bookings</h3>
        {bookings.map((b) => (
          <div key={b.id} className="list-row">
            <p style={{ margin: 0 }}>
              {b.user.name} booked {b.vehicle.name} ({b.startDate} to {b.endDate})
            </p>
            <span className={"status-badge status-" + (b.status === "ACTIVE" ? "AVAILABLE" : "BOOKED")}>
              {b.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AdminPage;

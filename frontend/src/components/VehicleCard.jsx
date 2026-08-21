import { useState } from "react";
import axios from "axios";
import { useUser } from "../context/UserContext";

function VehicleCard({ vehicle, onBooked }) {
  const { currentUser } = useUser();
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [message, setMessage] = useState("");

  const handleBook = () => {
    if (!startDate || !endDate) {
      setMessage("Please select both dates.");
      return;
    }

    axios.post(
      `http://localhost:8080/api/bookings/user/${currentUser.id}/vehicle/${vehicle.id}`,
      { startDate, endDate }
    )
      .then(() => {
        setMessage("Booked successfully!");
        onBooked();
      })
      .catch((error) => {
        setMessage(error.response?.data?.message || "Booking failed.");
      });
  };

  return (
    <div className="vehicle-card">
      <h3>{vehicle.name}</h3>
      <p>Type: {vehicle.type}</p>
      <p>Price per day: ₹{vehicle.pricePerDay}</p>
      <span className={"status-badge status-" + vehicle.status}>
        {vehicle.status}
      </span>

      {vehicle.status === "AVAILABLE" && currentUser && (
        <div className="form-group" style={{ marginTop: 12 }}>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
          <button className="btn" onClick={handleBook}>Book Now</button>
        </div>
      )}

      {vehicle.status === "AVAILABLE" && !currentUser && (
        <p className="message">Login to book this vehicle</p>
      )}

      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default VehicleCard;

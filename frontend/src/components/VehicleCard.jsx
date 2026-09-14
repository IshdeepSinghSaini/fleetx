import { useState, useEffect } from "react";
import axios from "axios";
import { useUser } from "../context/UserContext";

function VehicleCard({ vehicle, onBooked }) {
  const { currentUser } = useUser();
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [message, setMessage] = useState("");
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:8080/api/reviews/vehicle/${vehicle.id}`)
      .then((response) => {
        setReviews(response.data);
      });
  }, [vehicle.id]);

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
      <img
        src={vehicle.imageUrl || "https://placehold.co/300x180?text=No+Image"}
        alt={vehicle.name}
        className="vehicle-image"
        onError={(e) => {
          e.target.onerror = null;
          e.target.src = "https://placehold.co/300x180?text=No+Image";
        }}
      />
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

      {reviews.length > 0 && (
        <div style={{ marginTop: 12 }}>
          <p><strong>Reviews:</strong></p>
          {reviews.map((r) => (
            <p key={r.id} className="message">
              {r.rating}/5 — {r.comment}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}

export default VehicleCard;

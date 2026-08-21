import { useState, useEffect } from "react";
import axios from "axios";
import { useUser } from "../context/UserContext";

function MyBookingsPage() {
  const { currentUser } = useUser();
  const [bookings, setBookings] = useState([]);

  const fetchBookings = () => {
    axios.get(`http://localhost:8080/api/bookings/user/${currentUser.id}`)
      .then((response) => {
        setBookings(response.data);
      });
  };

  useEffect(() => {
    fetchBookings();
  }, []);

  const handleCancel = (bookingId) => {
    axios.put(`http://localhost:8080/api/bookings/${bookingId}/cancel`)
      .then(() => {
        fetchBookings();
      });
  };

  if (!currentUser) {
    return <p>Please login to see your bookings.</p>;
  }

  return (
    <div>
      <h2>My Bookings</h2>
      {bookings.map((booking) => (
        <div key={booking.id} className="card">
          <h3>{booking.vehicle.name}</h3>
          <p>From: {booking.startDate} To: {booking.endDate}</p>
          <p>Total: ₹{booking.totalPrice}</p>
          <p>Status: {booking.status}</p>

          {booking.status === "ACTIVE" && (
            <button className="btn" onClick={() => handleCancel(booking.id)}>
              Cancel Booking
            </button>
          )}
        </div>
      ))}
    </div>
  );
}

export default MyBookingsPage;

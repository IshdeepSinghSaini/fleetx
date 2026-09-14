import { useState, useEffect } from "react";
import axios from "axios";
import { useUser } from "../context/UserContext";
import ReviewForm from "../components/ReviewForm";
import PaymentForm from "../components/PaymentForm";

function MyBookingsPage() {
  const { currentUser } = useUser();
  const [bookings, setBookings] = useState([]);
  const [reviewingId, setReviewingId] = useState(null);
  const [payingId, setPayingId] = useState(null);

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
      <p className="section-title">My Bookings</p>
      {bookings.length === 0 && <p className="message">You have no bookings yet.</p>}
      {bookings.map((booking) => (
        <div key={booking.id} className="card">
          <h3>{booking.vehicle.name}</h3>
          <p>From: {booking.startDate} To: {booking.endDate}</p>
          <p>Total: ₹{booking.totalPrice}</p>
          <span className={"status-badge status-" + (booking.status === "ACTIVE" ? "AVAILABLE" : "BOOKED")}>
            {booking.status}
          </span>

          <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginTop: 14 }}>
            {booking.status === "ACTIVE" && (
              <button className="btn btn-danger" onClick={() => handleCancel(booking.id)}>
                Cancel Booking
              </button>
            )}

            {payingId !== booking.id && (
              <button className="btn" onClick={() => setPayingId(booking.id)}>
                Pay Now
              </button>
            )}

            {reviewingId !== booking.id && (
              <button className="btn btn-outline" onClick={() => setReviewingId(booking.id)}>
                Leave a Review
              </button>
            )}
          </div>

          {payingId === booking.id && <PaymentForm bookingId={booking.id} />}
          {reviewingId === booking.id && <ReviewForm bookingId={booking.id} />}
        </div>
      ))}
    </div>
  );
}

export default MyBookingsPage;

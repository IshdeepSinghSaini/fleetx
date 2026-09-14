import { useState } from "react";
import axios from "axios";

function PaymentForm({ bookingId }) {
  const [method, setMethod] = useState("CARD");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handlePay = () => {
    axios.post(`http://localhost:8080/api/payments/booking/${bookingId}?method=${method}`)
      .then((response) => {
        setResult(response.data);
      })
      .catch((error) => {
        setError(error.response?.data?.message || "Payment request failed.");
      });
  };

  if (error) {
    return <p className="message">{error}</p>;
  }

  if (result) {
    return (
      <p className="message">
        Payment {result.status} — ₹{result.amount}
      </p>
    );
  }

  return (
    <div className="form-group" style={{ marginTop: 10 }}>
      <select value={method} onChange={(e) => setMethod(e.target.value)}>
        <option value="CARD">Card</option>
        <option value="UPI">UPI</option>
        <option value="CASH">Cash</option>
      </select>
      <button className="btn" onClick={handlePay}>Pay Now</button>
    </div>
  );
}

export default PaymentForm;

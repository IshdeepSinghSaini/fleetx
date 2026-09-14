import { useState } from "react";
import axios from "axios";

function ReviewForm({ bookingId }) {
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");
  const [message, setMessage] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    axios.post(`http://localhost:8080/api/reviews/booking/${bookingId}`, {
      rating: Number(rating),
      comment: comment,
    })
      .then(() => {
        setMessage("Review submitted, thank you!");
        setSubmitted(true);
      })
      .catch((error) => {
        setMessage(error.response?.data?.message || "Could not submit review.");
      });
  };

  if (submitted) {
    return <p className="message">{message}</p>;
  }

  return (
    <form onSubmit={handleSubmit} className="form-group" style={{ marginTop: 10 }}>
      <select value={rating} onChange={(e) => setRating(e.target.value)}>
        <option value="5">5 - Excellent</option>
        <option value="4">4 - Good</option>
        <option value="3">3 - Okay</option>
        <option value="2">2 - Poor</option>
        <option value="1">1 - Bad</option>
      </select>
      <input
        placeholder="Write a comment"
        value={comment}
        onChange={(e) => setComment(e.target.value)}
      />
      <button type="submit" className="btn">Submit Review</button>
      {message && <p className="message">{message}</p>}
    </form>
  );
}

export default ReviewForm;

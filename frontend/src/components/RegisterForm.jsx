import { useState } from "react";
import axios from "axios";

function RegisterForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [phone, setPhone] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    axios.post("http://localhost:8080/api/users/register", {
      name: name,
      email: email,
      password: password,
      phone: phone,
    })
      .then((response) => {
        setMessage("Registered successfully! Welcome, " + response.data.name);
      })
      .catch((error) => {
        setMessage("Registration failed. Please try again.");
      });
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit} className="form-group">
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input
          type="text"
          placeholder="Phone"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
        />
        <button type="submit" className="btn">Register</button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default RegisterForm;

import { useState } from "react";
import axios from "axios";
import { useUser } from "../context/UserContext";

function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const { login } = useUser();

  const handleSubmit = (e) => {
    e.preventDefault();

    axios.post("http://localhost:8080/api/users/login", {
      email: email,
      password: password,
    })
      .then((response) => {
        login(response.data);
        setMessage("Welcome back, " + response.data.name + "!");
      })
      .catch((error) => {
        setMessage("Invalid email or password.");
      });
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit} className="form-group">
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
        <button type="submit" className="btn">Login</button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default LoginForm;
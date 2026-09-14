import { createContext, useState, useContext } from "react";
import axios from "axios";

const UserContext = createContext();

function applyAuthHeader(token) {
  if (token) {
    axios.defaults.headers.common["Authorization"] = "Bearer " + token;
  } else {
    delete axios.defaults.headers.common["Authorization"];
  }
}

export function UserProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(() => {
    const saved = localStorage.getItem("fleetx_user");
    const token = localStorage.getItem("fleetx_token");
    return saved && token ? JSON.parse(saved) : null;
  });

  applyAuthHeader(localStorage.getItem("fleetx_token"));

  const login = (user, token) => {
    setCurrentUser(user);
    localStorage.setItem("fleetx_user", JSON.stringify(user));
    localStorage.setItem("fleetx_token", token);
    applyAuthHeader(token);
  };

  const logout = () => {
    setCurrentUser(null);
    localStorage.removeItem("fleetx_user");
    localStorage.removeItem("fleetx_token");
    applyAuthHeader(null);
  };

  return (
    <UserContext.Provider value={{ currentUser, login, logout }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  return useContext(UserContext);
}

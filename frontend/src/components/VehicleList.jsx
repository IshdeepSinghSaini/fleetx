import { useState, useEffect } from "react";
import axios from "axios";
import VehicleCard from "./VehicleCard";

function VehicleList() {
  const [vehicles, setVehicles] = useState([]);
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState("ALL");

  const fetchVehicles = () => {
    axios.get("http://localhost:8080/api/vehicles")
      .then((response) => {
        setVehicles(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    fetchVehicles();
  }, []);

  const types = ["ALL", ...new Set(vehicles.map((v) => v.type))];

  const filtered = vehicles.filter((v) => {
    const matchesSearch = v.name.toLowerCase().includes(search.toLowerCase());
    const matchesType = typeFilter === "ALL" || v.type === typeFilter;
    return matchesSearch && matchesType;
  });

  return (
    <div>
      <h2>Available Vehicles</h2>

      <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginBottom: 20 }}>
        <input
          placeholder="Search by name..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ padding: "10px 14px", border: "1px solid var(--border)", borderRadius: 8, minWidth: 220 }}
        />
        <select
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
          style={{ padding: "10px 14px", border: "1px solid var(--border)", borderRadius: 8 }}
        >
          {types.map((t) => (
            <option key={t} value={t}>{t === "ALL" ? "All types" : t}</option>
          ))}
        </select>
      </div>

      {filtered.length === 0 && <p className="message">No vehicles match your search.</p>}

      <div className="vehicle-grid">
        {filtered.map((vehicle) => (
          <VehicleCard key={vehicle.id} vehicle={vehicle} onBooked={fetchVehicles} />
        ))}
      </div>
    </div>
  );
}

export default VehicleList;

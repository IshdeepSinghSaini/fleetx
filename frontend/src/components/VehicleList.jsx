import { useState, useEffect } from "react";
import axios from "axios";
import VehicleCard from "./VehicleCard";

function VehicleList() {
  const [vehicles, setVehicles] = useState([]);

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

  return (
    <div>
      <h2>Available Vehicles</h2>
      <div className="vehicle-grid">
        {vehicles.map((vehicle) => (
          <VehicleCard key={vehicle.id} vehicle={vehicle} onBooked={fetchVehicles} />
        ))}
      </div>
    </div>
  );
}

export default VehicleList;

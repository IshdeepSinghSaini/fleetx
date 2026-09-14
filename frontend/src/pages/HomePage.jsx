import VehicleList from "../components/VehicleList";

function HomePage() {
  return (
    <div>
      <div className="hero">
        <h1>Find your next ride</h1>
        <p>Browse available cars and bikes, book instantly, manage everything in one place.</p>
      </div>
      <div className="page-inner">
        <VehicleList />
      </div>
    </div>
  );
}

export default HomePage;

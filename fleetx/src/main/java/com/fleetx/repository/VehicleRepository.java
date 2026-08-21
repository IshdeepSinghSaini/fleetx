package com.fleetx.repository;

import com.fleetx.entity.Vehicle;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface VehicleRepository extends JpaRepository<Vehicle, Long> {

    List<Vehicle> findByType(String type);

    List<Vehicle> findByStatus(Vehicle.Status status);

    List<Vehicle> findByLocation(String location);
}

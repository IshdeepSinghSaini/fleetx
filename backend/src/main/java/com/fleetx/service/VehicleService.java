package com.fleetx.service;

import com.fleetx.entity.Vehicle;
import com.fleetx.repository.VehicleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class VehicleService {

    @Autowired
    private VehicleRepository vehicleRepository;

    public Vehicle addVehicle(Vehicle vehicle) {
        return vehicleRepository.save(vehicle);
    }

    public List<Vehicle> getAllVehicles() {
        return vehicleRepository.findAll();
    }

    public Vehicle getVehicleById(Long id) {
        return vehicleRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Vehicle not found"));
    }

    public List<Vehicle> getVehiclesByType(String type) {
        return vehicleRepository.findByType(type);
    }

    public List<Vehicle> getAvailableVehicles() {
        return vehicleRepository.findByStatus(Vehicle.Status.AVAILABLE);
    }

    public List<Vehicle> getVehiclesByLocation(String location) {
        return vehicleRepository.findByLocation(location);
    }

    public Vehicle updateVehicle(Long id, Vehicle updatedVehicle) {
        Vehicle vehicle = getVehicleById(id);
        vehicle.setName(updatedVehicle.getName());
        vehicle.setType(updatedVehicle.getType());
        vehicle.setPricePerDay(updatedVehicle.getPricePerDay());
        vehicle.setSeats(updatedVehicle.getSeats());
        vehicle.setLocation(updatedVehicle.getLocation());
        vehicle.setStatus(updatedVehicle.getStatus());
        vehicle.setImageUrl(updatedVehicle.getImageUrl());
        return vehicleRepository.save(vehicle);
    }

    public void deleteVehicle(Long id) {
        try {
            vehicleRepository.deleteById(id);
        } catch (DataIntegrityViolationException e) {
            throw new RuntimeException("Cannot delete this vehicle — it has existing bookings, maintenance logs, or reviews.");
        }
    }
}

package com.fleetx.service;

import com.fleetx.entity.MaintenanceLog;
import com.fleetx.entity.Vehicle;
import com.fleetx.repository.MaintenanceLogRepository;
import com.fleetx.repository.VehicleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Service
public class MaintenanceService {

    @Autowired
    private MaintenanceLogRepository maintenanceLogRepository;

    @Autowired
    private VehicleRepository vehicleRepository;

    public MaintenanceLog startMaintenance(Long vehicleId, MaintenanceLog logRequest) {
        Vehicle vehicle = vehicleRepository.findById(vehicleId)
                .orElseThrow(() -> new RuntimeException("Vehicle not found"));

        MaintenanceLog log = new MaintenanceLog();
        log.setVehicle(vehicle);
        log.setDescription(logRequest.getDescription());
        log.setCost(logRequest.getCost());
        log.setStartDate(logRequest.getStartDate());

        vehicle.setStatus(Vehicle.Status.MAINTENANCE);
        vehicleRepository.save(vehicle);

        return maintenanceLogRepository.save(log);
    }

    public MaintenanceLog completeMaintenance(Long logId) {
        MaintenanceLog log = maintenanceLogRepository.findById(logId)
                .orElseThrow(() -> new RuntimeException("Maintenance log not found"));

        log.setEndDate(LocalDate.now());

        Vehicle vehicle = log.getVehicle();
        vehicle.setStatus(Vehicle.Status.AVAILABLE);
        vehicleRepository.save(vehicle);

        return maintenanceLogRepository.save(log);
    }

    public List<MaintenanceLog> getAllLogs() {
        return maintenanceLogRepository.findAll();
    }

    public List<MaintenanceLog> getLogsByVehicle(Long vehicleId) {
        return maintenanceLogRepository.findByVehicleId(vehicleId);
    }
}

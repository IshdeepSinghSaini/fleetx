package com.fleetx.controller;

import com.fleetx.entity.MaintenanceLog;
import com.fleetx.service.MaintenanceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/maintenance")
public class MaintenanceController {

    @Autowired
    private MaintenanceService maintenanceService;

    @PostMapping("/vehicle/{vehicleId}")
    public MaintenanceLog startMaintenance(@PathVariable Long vehicleId, @RequestBody MaintenanceLog logRequest) {
        return maintenanceService.startMaintenance(vehicleId, logRequest);
    }

    @PutMapping("/{id}/complete")
    public MaintenanceLog completeMaintenance(@PathVariable Long id) {
        return maintenanceService.completeMaintenance(id);
    }

    @GetMapping
    public List<MaintenanceLog> getAllLogs() {
        return maintenanceService.getAllLogs();
    }

    @GetMapping("/vehicle/{vehicleId}")
    public List<MaintenanceLog> getLogsByVehicle(@PathVariable Long vehicleId) {
        return maintenanceService.getLogsByVehicle(vehicleId);
    }
}

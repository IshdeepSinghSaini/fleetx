package com.fleetx.service;

import com.fleetx.entity.Booking;
import com.fleetx.entity.User;
import com.fleetx.entity.Vehicle;
import com.fleetx.repository.BookingRepository;
import com.fleetx.repository.UserRepository;
import com.fleetx.repository.VehicleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.temporal.ChronoUnit;
import java.util.List;

@Service
public class BookingService {

    @Autowired
    private BookingRepository bookingRepository;

    @Autowired
    private VehicleRepository vehicleRepository;

    @Autowired
    private UserRepository userRepository;

    public Booking createBooking(Long userId, Long vehicleId, Booking bookingRequest) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));

        Vehicle vehicle = vehicleRepository.findById(vehicleId)
                .orElseThrow(() -> new RuntimeException("Vehicle not found"));

        if (vehicle.getStatus() != Vehicle.Status.AVAILABLE) {
            throw new RuntimeException("Vehicle is not available for booking");
        }

        long days = ChronoUnit.DAYS.between(bookingRequest.getStartDate(), bookingRequest.getEndDate());
        if (days <= 0) {
            throw new RuntimeException("End date must be after start date");
        }

        Booking booking = new Booking();
        booking.setUser(user);
        booking.setVehicle(vehicle);
        booking.setStartDate(bookingRequest.getStartDate());
        booking.setEndDate(bookingRequest.getEndDate());
        booking.setTotalPrice(days * vehicle.getPricePerDay());
        booking.setStatus(Booking.Status.ACTIVE);

        vehicle.setStatus(Vehicle.Status.BOOKED);
        vehicleRepository.save(vehicle);

        return bookingRepository.save(booking);
    }

    public List<Booking> getAllBookings() {
        return bookingRepository.findAll();
    }

    public List<Booking> getBookingsByUser(Long userId) {
        return bookingRepository.findByUserId(userId);
    }

    public Booking cancelBooking(Long bookingId) {
        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new RuntimeException("Booking not found"));

        booking.setStatus(Booking.Status.CANCELLED);

        Vehicle vehicle = booking.getVehicle();
        vehicle.setStatus(Vehicle.Status.AVAILABLE);
        vehicleRepository.save(vehicle);

        return bookingRepository.save(booking);
    }
}

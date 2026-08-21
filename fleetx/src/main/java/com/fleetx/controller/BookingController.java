package com.fleetx.controller;

import com.fleetx.entity.Booking;
import com.fleetx.service.BookingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/bookings")
public class BookingController {

    @Autowired
    private BookingService bookingService;

    @PostMapping("/user/{userId}/vehicle/{vehicleId}")
    public Booking createBooking(@PathVariable Long userId,
                                  @PathVariable Long vehicleId,
                                  @RequestBody Booking bookingRequest) {
        return bookingService.createBooking(userId, vehicleId, bookingRequest);
    }

    @GetMapping
    public List<Booking> getAllBookings() {
        return bookingService.getAllBookings();
    }

    @GetMapping("/user/{userId}")
    public List<Booking> getBookingsByUser(@PathVariable Long userId) {
        return bookingService.getBookingsByUser(userId);
    }

    @PutMapping("/{id}/cancel")
    public Booking cancelBooking(@PathVariable Long id) {
        return bookingService.cancelBooking(id);
    }
}

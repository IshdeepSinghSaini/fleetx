package com.fleetx.service;

import com.fleetx.entity.Booking;
import com.fleetx.entity.Payment;
import com.fleetx.repository.BookingRepository;
import com.fleetx.repository.PaymentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Random;

@Service
public class PaymentService {

    @Autowired
    private PaymentRepository paymentRepository;

    @Autowired
    private BookingRepository bookingRepository;

    public Payment makePayment(Long bookingId, Payment.Method method) {
        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new RuntimeException("Booking not found"));

        Payment existing = paymentRepository.findByBookingId(bookingId);
        if (existing != null) {
            throw new RuntimeException("This booking already has a payment recorded (status: " + existing.getStatus() + ")");
        }

        Payment payment = new Payment();
        payment.setBooking(booking);
        payment.setAmount(booking.getTotalPrice());
        payment.setPaymentMethod(method);

        boolean success = new Random().nextInt(100) < 90;
        payment.setStatus(success ? Payment.Status.SUCCESS : Payment.Status.FAILED);

        return paymentRepository.save(payment);
    }

    public List<Payment> getAllPayments() {
        return paymentRepository.findAll();
    }

    public Payment getPaymentById(Long id) {
        return paymentRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Payment not found"));
    }
}

package com.fleetx.controller;

import com.fleetx.entity.Payment;
import com.fleetx.service.PaymentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/payments")
public class PaymentController {

    @Autowired
    private PaymentService paymentService;

    @PostMapping("/booking/{bookingId}")
    public Payment makePayment(@PathVariable Long bookingId, @RequestParam Payment.Method method) {
        return paymentService.makePayment(bookingId, method);
    }

    @GetMapping
    public List<Payment> getAllPayments() {
        return paymentService.getAllPayments();
    }

    @GetMapping("/{id}")
    public Payment getPaymentById(@PathVariable Long id) {
        return paymentService.getPaymentById(id);
    }
}

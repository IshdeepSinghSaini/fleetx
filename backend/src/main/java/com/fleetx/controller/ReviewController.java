package com.fleetx.controller;

import com.fleetx.entity.Review;
import com.fleetx.service.ReviewService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/reviews")
public class ReviewController {

    @Autowired
    private ReviewService reviewService;

    @PostMapping("/booking/{bookingId}")
    public Review addReview(@PathVariable Long bookingId, @RequestBody Review reviewRequest) {
        return reviewService.addReview(bookingId, reviewRequest);
    }

    @GetMapping("/vehicle/{vehicleId}")
    public List<Review> getReviewsByVehicle(@PathVariable Long vehicleId) {
        return reviewService.getReviewsByVehicle(vehicleId);
    }

    @GetMapping
    public List<Review> getAllReviews() {
        return reviewService.getAllReviews();
    }
}

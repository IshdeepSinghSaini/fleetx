package com.fleetx.service;

import com.fleetx.entity.Booking;
import com.fleetx.entity.Review;
import com.fleetx.repository.BookingRepository;
import com.fleetx.repository.ReviewRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ReviewService {

    @Autowired
    private ReviewRepository reviewRepository;

    @Autowired
    private BookingRepository bookingRepository;

    public Review addReview(Long bookingId, Review reviewRequest) {
        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new RuntimeException("Booking not found"));

        if (reviewRepository.findByBookingId(bookingId) != null) {
            throw new RuntimeException("This booking has already been reviewed");
        }

        Review review = new Review();
        review.setBooking(booking);
        review.setUser(booking.getUser());
        review.setVehicle(booking.getVehicle());
        review.setRating(reviewRequest.getRating());
        review.setComment(reviewRequest.getComment());

        return reviewRepository.save(review);
    }

    public List<Review> getReviewsByVehicle(Long vehicleId) {
        return reviewRepository.findByVehicleId(vehicleId);
    }

    public List<Review> getAllReviews() {
        return reviewRepository.findAll();
    }
}

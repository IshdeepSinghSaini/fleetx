-- FleetX Analytics Queries
-- =========================

-- 1. Total Revenue
SELECT SUM(amount) AS total_revenue
FROM payments
WHERE status = 'SUCCESS';

-- 2. Most Popular Vehicles (by number of bookings)
SELECT v.name, v.type, COUNT(b.id) AS total_bookings
FROM vehicles v
LEFT JOIN bookings b ON b.vehicle_id = v.id
GROUP BY v.id, v.name, v.type
ORDER BY total_bookings DESC;

-- 3. Cancellation Rate
SELECT
    COUNT(*) AS total_bookings,
    COUNT(*) FILTER (WHERE status = 'CANCELLED') AS cancelled_bookings,
    ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'CANCELLED') / COUNT(*), 2) AS cancellation_rate_pct
FROM bookings;

-- 4. Vehicle Utilization (total booked days per vehicle)
SELECT
    v.name,
    v.status,
    COALESCE(SUM(b.end_date - b.start_date) FILTER (WHERE b.status != 'CANCELLED'), 0) AS total_booked_days
FROM vehicles v
LEFT JOIN bookings b ON b.vehicle_id = v.id
GROUP BY v.id, v.name, v.status
ORDER BY total_booked_days DESC;

-- 5. Top Customers (by bookings and total spend)
SELECT
    u.name,
    u.email,
    COUNT(b.id) AS total_bookings,
    COALESCE(SUM(b.total_price) FILTER (WHERE b.status != 'CANCELLED'), 0) AS total_spend
FROM users u
JOIN bookings b ON b.user_id = u.id
GROUP BY u.id, u.name, u.email
ORDER BY total_spend DESC;

-- 6. Average Booking Value
SELECT ROUND(AVG(total_price)::numeric, 2) AS avg_booking_value
FROM bookings
WHERE status != 'CANCELLED';

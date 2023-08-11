-- Show all seat 

select * from booking_seat;



-- Filter Pending Seat from SeatAvailability
SELECT *
FROM seatavailability
WHERE
    user_id = 1
    AND hall_id = 1
    AND show_date = '2023-08-29'
    AND movie_id = 2
    AND seat_status = 'pending'
    AND payment_status = false;

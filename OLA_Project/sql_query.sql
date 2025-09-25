create database OLA_db;
use OLA_db;

select count(*) from ola_rides;

select * from ola_rides limit 5;



-- 1. Retrieve all successful bookings
select * from ola_rides where Booking_Status = "Success";

-- 2. Find the average ride distance for each vehicle type
select
	Vehicle_Type,
    round(avg(Ride_Distance),2) as avg_ride_distance
from 
	ola_rides
group by Vehicle_Type
order by avg_ride_distance desc;

-- 3. Get the total number of cancelled rides by customers
select count(*) as total_rides
from ola_rides 
where Booking_status = "Canceled by Customer";

-- 4. List the top 5 customers who booked the highest number of rides
select Customer_ID, 
	count(*) as total_rides
from ola_rides
group by Customer_ID
order by total_rides desc
limit 5;

-- 5. Get the number of rides cancelled by drivers due to personal and car-related issues
select count(*) as total_rides
from ola_rides
where Canceled_Rides_by_Driver = 'Personal & Car related issue';

-- 6. Find the maximum and minimum driver ratings for Prime Sedan bookings
select 
	Vehicle_Type,
	round(max(Driver_Ratings),2) as max_ratings,
    round(min(Driver_Ratings),2) as min_ratings
from ola_rides
where Vehicle_Type = 'Prime Sedan';

-- 7. Retrieve all rides where payment was made using UPI
select Payment_Method, count(*) as total_rides
from ola_rides
where Payment_Method = 'UPI';

-- 8. Find the average customer rating per vehicle type
select
	Vehicle_Type,
    round(avg(Customer_Rating),2) as avg_rating
from ola_rides
group by Vehicle_Type
order by avg_rating desc;

-- 9. Calculate the total booking value of rides completed successfully
select
	Booking_Status,
    sum(Booking_Value) as total_booking_value
from ola_rides
where Booking_Status = 'Success';

-- 10. List all incomplete rides along with the reason
select * 
from ola_rides
where Incomplete_Rides = 'Yes' and Incomplete_Rides_Reason <> 'Unknown';

-- 1. Overall 
		-- Ride Volume Over Time
create or replace view ride_volume_over_time as
select 
	date(Date) as ride_date,
    count(*) as total_rides
from ola_rides
group by date(Date)
order by ride_date;


-- Booking Status Breakdown 
create or replace view booking_status_breakdown as
select
	Booking_Status,
    count(*) as total_rides
from ola_rides
group by Booking_Status
order by total_rides desc;

-- 2. Vehicle Type 
	-- Top 5 Vehicle Types by Ride Distance
create or replace view top5_vehicle_type_by_distance as
select
	Vehicle_Type,
    sum(Ride_Distance) as total_distance
from ola_rides
group by Vehicle_Type
order by total_distance desc;

-- 3. Revenue
 -- Revenue by Payment Method
create or replace view revenue_by_payment_method as
select
	Payment_Method,
    sum(Booking_Value) as total_revenue
from ola_rides
where Booking_Status = 'Success'
group by Payment_Method
order by total_revenue desc;


-- Top 5 Customers by Total Booking Value
create or replace view top5_customers_revenue as
select
	Customer_ID,
    sum(Booking_Value) as total_booking_value
from ola_rides
where Booking_Status = 'Success'
group by Customer_ID
order by total_booking_value desc
limit 5;

-- Ride Distance Distribution Per Day
create or replace view ride_distance_distribution_per_day as
select
	date(Date) as ride_date,
    avg(Ride_Distance) as avg_distance,
    min(Ride_Distance) as min_distance,
    max(Ride_Distance) as max_distance
from ola_rides
group by date(Date)
order by ride_date;

-- 4. Cancellation
-- Cancelled Rides Reasons (Customer) 
create or replace view canceled_rides_customer as
select 
	Canceled_Rides_by_Customer as cancel_reason,
    count(*) as cancel_count
from ola_rides
where Booking_Status = 'Canceled by Customer'
	and Canceled_Rides_by_Customer <> 'Unknown'
group by Canceled_Rides_by_Customer
order by cancel_count desc;

-- cancelled Rides Reasons(Drivers) 
create or replace view canceled_rides_driver as
select
	Canceled_Rides_by_Driver as cancel_reason,
    count(*) as cancel_count
from ola_rides
where Booking_Status = 'Canceled by Driver'
	and Canceled_Rides_by_Driver <> 'Unknown'
group by Canceled_Rides_by_Driver
order by cancel_count desc;


-- 5. Ratings 
-- Driver Ratings 
create or replace view driver_ratings_summary as
select
	Vehicle_Type,
    round(avg(Driver_Ratings),2) as avg_driver_ratings,
    max(Driver_Ratings) as max_driver_ratings,
    min(Driver_Ratings) as min_driver_ratings
from ola_rides
group by Vehicle_Type
order by avg_driver_ratings desc;


-- Customer Ratings 
create or replace view customer_ratings_summary as
select
	Vehicle_Type,
    round(avg(Customer_Rating),2) as avg_customer_ratings,
    max(Customer_Rating) as max_customer_ratings,
    min(Customer_Rating) as min_customer_ratings
from ola_rides
group by Vehicle_Type
order by avg_customer_ratings desc;    
    


select * from booking_status_breakdown;

# apiteam04

Flask RESTful API for Sports resources booking Application<br>
This API has been deployed onto Heroku.<br>

The main purpose of this API is for students to be able to book sports resources and for the admins to keep tab on the availablity of resources along with streamlining the fine process.<br>

Link:https://sport-resources-booking-api.herokuapp.com/<br>
Everyone can access these endpoints:<br>
a)/register-POST to the users table<br><br>
b) /login-takes a JSON object with 'username' and 'password' and gives back JWT token if exists in Users table. The JWT shall be used to access all the end points. For all the endpoints an Authorization Header should be included with value 'Bearer '.<br>


The/adminLogin endpoint is only meant for the admins and momentarily there is one admin in the admin table who can make changes in the respective tables. This table also takes a JSON object with 'username' and 'password' and gives back JWT token if exists in Admin table. The JWT shall be used to access all the end points. For all the endpoints an Authorization Header should be included with value 'Bearer '.<br><br>

/ResourcesPresent- GET request from the resource table to give the number of a specific resource present obtained by the id.<br><br>
/AddExtraResource- The admin can only make changes after providing the access token. Updates the resources table and increases the count value when a new resource is bought by the administration.<br><br>
/DeleteResource-  The admin can only make changes after providing the access token. Updates the resources table and decreases the count value when a new resource is bought by the administration.<br><br>
/userBookingslog<br><br>
/userDue-GET request from the ----- table in order to receive the due of a student if any<br><br>
/cancelBooking- POST request to first check if the booking exists and then change it's status to unbooked and give a message to the user.<br><br>
/resourceDetails- GET request to receive all the details of a given resource from the resource table with the help of an ID.<br><br>
/incrementByOne-The admin can only make changes after providing the access token. Updates the resources table and increases the count value by 1 when a new resource is bought by the administration.<br><br>
/incrementByValue- The admin can only make changes after providing the access token. Updates the resources table and increases the count value when a new resource is bought by the administration.<br><br>
/decrementByOne- The admin can only make changes after providing the access token. Updates the resources table and deecreases the count value by 1 when a new resource is bought by the administration.<br><br>
/decrementByValue- GET request which the admin can only make after providing the access token. Updates the resources table and decreases the count value when a new resource is bought by the administration.<br><br>
/issueResource-<br><br>
/acceptResource- GET request to obtain the data regarding the date of issue and also update the valuee of the resources left in the resource table.<br><br>
/bookingHistory-GET request to obtain the log of all bookings made from the BookingHistory1 view.<br><br>
/issuedBookings-GET request to obtain the log of all bookings made on the current day from the BookingHistory1 view.<br><br>
/blockedUsers- GET request to receive the users who have been blocked so as to not issue any more resources<br><br>
/unblockUser-GET request updating the database to obtain the status of the user and to change the status of due of the user when a user pays their dues. <br><br>
/blockUser-GET request to update the fine next to the id of a user using the id.<br><br>
/bookResource-<br><br>
/rejectBooking-GET request to check if the user has dues and if dues exist, the booking cannot be made <br><br>
/returnedHistory-GET request to obtain the log of all the users who returned booked resources till that time from the BookingHistory2 view.<br><br>
/notreturnedHistory'- GET request to obtain the log of all the users who hadn't returned booked resources till that time from the BookingHistory2 view.<br><br>
/allBookings-GET request to receive all the bookings from the view BookingHistory1.<br><br>



# apiteam04

Flask RESTful API for Sports resources booking Application<br>
This API has been deployed onto Heroku.<br>

The main purpose of this API is for students to be able to book sports resources and for the admins to keep tab on the availablity of resources along with streamlining the fine process.<br>

Link:<br>
Everyone can access these endpoints:<br>
a)/register-POST to the users table<br>
b) /login-takes a JSON object with 'username' and 'password' and gives back JWT if exists in Users table. The JWT shall be used to access all the end points. For all the endpoints an Authorization Header should be included with value 'Bearer '.<br>


The/adminLogin endpoint is only meant for the admins and momentarily there is one admin in the admin table who can make changes in the respective tables. This table also takes a JSON object with 'username' and 'password' and gives back JWT if exists in Admin table. The JWT shall be used to access all the end points. For all the endpoints an Authorization Header should be included with value 'Bearer '.<br>

/ResourcesPresent- GET request from the resource table to give the number of a specific resource present obtained by the id.<br>
/AddExtraResource- The admin can only make changes after providing the access token. Updates the resources table and increases the count value when a new resource is bought by the administration.<br>
/DeleteResource-  The admin can only make changes after providing the access token. Updates the resources table and decreases the count value when a new resource is bought by the administration.<br>
/userBookingslog<br>
/userDue-GET request from the ----- table in order to receive the due of a student if any
/cancelBooking<br>
/resourceDetails- GET request to receive all the details of a given resource from the resource table with the help of an ID.<br>
/incrementByOne<br>
/incrementByValue- The admin can only make changes after providing the access token. Updates the resources table and increases the count value when a new resource is bought by the administration.<br>
/decrementByOne<br>
/decrementByValue- GET request which the admin can only make after providing the access token. Updates the resources table and decreases the count value when a new resource is bought by the administration.<br>
/issueResource<br>
/acceptResource- GET request to update the <br>
/bookingHistory<br>
/issuedBookings<br>
/blockedUsers- GET request to receive the users who have been blocked so as to not issue any more resources<br>
/unblockUser-POST request updating the database to change the status of due the user when a user pays their dues <br>
api.add_resource(blockUser,'/blockUser')<br>
api.add_resource(bookResource,'/bookResource')<br>
api.add_resource(bookingRequests,'/bookingRequests')<br>
api.add_resource(rejectBooking,'/rejectBooking')<br>
api.add_resource(check,'/check')<br>
api.add_resource(returnedHistory,'/returnedHistory')<br>
api.add_resource(notreturnedHistory,'/notreturnedHistory')<br>
/allBookings-GET request to receive all the bookings from the table BookingHistory1.<br>



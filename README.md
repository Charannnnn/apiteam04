# apiteam04

Flask RESTful API for Sports resources booking Application
This API has been deployed onto Heroku.

The main purpose of this API is for students to be able to book sports resources and for the admins to keep tab on the availablity of resources along with streamlining the fine process.

Link:
Everyone can access these endpoints:
a)/register-POST to the users table
b) /login-takes a JSON object with 'username' and 'password' and gives back JWT if exists in Users table. The JWT shall be used to access all the end points. For all the endpoints an Authorization Header should be included with value 'Bearer '.


The/adminLogin endpoint is only meant for the admins and momentarily there is one admin in the admin table who can make changes in the respective tables. This table also takes a JSON object with 'username' and 'password' and gives back JWT if exists in Admin table. The JWT shall be used to access all the end points. For all the endpoints an Authorization Header should be included with value 'Bearer '.

/ResourcesPresent- GET request from the resource table to give the number of a specific resource present obtained by the id.
/AddExtraResource- The admin can only make changes after providing the access token. Updates the resources table and increases the count value when a new resource is bought by the administration.
/DeleteResource-  The admin can only make changes after providing the access token. Updates the resources table and decreases the count value when a new resource is bought by the administration.
/userBookingslog
/userDue-GET request from the ----- table in order to receive the due of a student if any
/cancelBooking
/resourceDetails- GET request to receive all the details of a given resource from the resource table with the help of an ID.
/incrementByOne
/incrementByValue- The admin can only make changes after providing the access token. Updates the resources table and increases the count value when a new resource is bought by the administration.
/decrementByOne
/decrementByValue- GET request which the admin can only make after providing the access token. Updates the resources table and decreases the count value when a new resource is bought by the administration.
/issueResource
/acceptResource- GET request to update the 
/bookingHistory
/issuedBookings
/blockedUsers- GET request to receive the users who have been blocked so as to not issue any more resources
/unblockUser-POST request updating the database to change the status of due the user when a user pays their dues 
api.add_resource(blockUser,'/blockUser')
api.add_resource(bookResource,'/bookResource')
api.add_resource(bookingRequests,'/bookingRequests')
api.add_resource(rejectBooking,'/rejectBooking')
api.add_resource(check,'/check')
api.add_resource(returnedHistory,'/returnedHistory')
api.add_resource(notreturnedHistory,'/notreturnedHistory')
/allBookings-GET request to receive all the bookings from the table BookingHistory1.



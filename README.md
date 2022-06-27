# backend template



CURRENT API's:
# USER MANAGEMENT APIs

```
/api/register/ - POST - Register a new user
/api/login/ - POST - Login a user
/api/logout/ - POST - Logout a user
/api/user/ - GET - Get user details
/api/user/ -  PUT - Update a user's profile
/api/update/address/ - PUT - Update a user's address
/api/confirm/email/ - PUT - Confirm a user's email
/api/private/ - GET - Get a protected page
```

User management APIs that allows users to:
1. API to Register (email, first_name, and password)
2. Sends a verification email to the customer
3. API to verify the email token and Login API
4. API for customers to update their profiles (middle_name, last_name, dob, nationality, phone_number)
5. API for the users to create their residential address (Country, City, state/province, zip)
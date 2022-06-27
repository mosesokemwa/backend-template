# backend template

### Description
User CMS module for managing user details and auth suing JWT


### Usage
```
$ python3 -m venv venv/
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python3 manage.py runserver
```
The above will start the server on (localhost:8000)[http://localhost:8000]

### Running tests
```
$ python3 manage.py test
```

### CURRENT API's:
#### USER MANAGEMENT APIs

```
/api/register/ - POST - Register a new user with username, email and password
/api/login/ - POST - Login a user with username and password
/api/user/ - GET - Get user details of the logged in user
/api/user/ -  PUT - Update a user's profile details
/api/update/address/ - PUT - Update a user's address details
/api/confirm/email/ - PUT - Confirm a user's email address(currently printing the confirmation email on console)
/api/private/ - GET - Get a protected page with JWT token
```

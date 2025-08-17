




______________________________API Testing with Postman  Register a User_______________________________

**Endpoint: POST /api/register/**

Request Body:

json
`{
    "username": "newuser",
    "password": "NewPass1234"
}`

Response:
json{"success": true}

====================================success

**Login to Get Token**

Endpoint: POST /api/token/
Request Body:
json
`{
    "username": "newuser",
    "password": "NewPass1234"
}`

Response:
json
`{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}`

Action: Use the access token in the Authorization header (Bearer your_access_token) for subsequent requests.

================================success

**Get Form Fields**

Endpoint: GET /api/form-fields/
Headers: Authorization: Bearer your_access_token
Response:

`json[
    {
        "id": 3,
        "label": "salary",
        "field_type": "text",
        "order": 0,
        "is_required": false,
        "options": [],
        "created_by": 3
    },
    {
        "id": 10,
        "label": "salary",
        "field_type": "text",
        "order": 0,
        "is_required": false,
        "options": [],
        "created_by": 1
    },
    {
        "id": 11,
        "label": "dddeddd",
        "field_type": "text",
        "order": 1,
        "is_required": false,
        "options": [],
        "created_by": 1
    },
    {
        "id": 12,
        "label": "dddddd",
        "field_type": "text",
        "order": 2,
        "is_required": false,
        "options": [],
        "created_by": 1
    },
    {
        "id": 13,
        "label": "defr3frf",
        "field_type": "text",
        "order": 3,
        "is_required": false,
        "options": [],
        "created_by": 1
    }
`

=======================================================================success

**Get All Employees**

Endpoint: GET /api/employees/
Headers: Authorization: Bearer your_access_token
Response:

`json[
    {
        "id": 1,
        "emp_id": "a1b2c3d4e5",
        "data": {"name": "John Doe"},
        "created_by": 1,
        "created_at": "2025-08-15T14:35:00Z",
        "updated_at": "2025-08-15T14:35:00Z",
        "role": "Developer",
        "designation": "Junior Developer",
        "reporting_manager": null
    },
    {
        "id": 2,
        "emp_id": "f6g7h8i9j0",
        "data": {"name": "Jane Smith"},
        "created_by": 1,
        "created_at": "2025-08-15T14:35:01Z",
        "updated_at": "2025-08-15T14:35:01Z",
        "role": "Manager",
        "designation": "Senior Manager",
        "reporting_manager": 1
    }
]
`
===================================================success
**Get Specific Employee**

Endpoint: GET /api/employees/5/
Headers: Authorization: Bearer your_access_token
Response:

`json{
    "id": 1,
    "emp_id": "a1b2c3d4e5",
    "data": {"name": "John Doe"},
    "created_by": 1,
    "created_at": "2025-08-15T14:35:00Z",
    "updated_at": "2025-08-15T14:35:00Z",
    "role": "Developer",
    "designation": "Junior Manager",
    "reporting_manager": null
}
`

=========================================
**Create New Employee**

Endpoint: POST /api/employees/
Headers: Authorization: Bearer your_access_token
Request Body:
`
json{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "address": "123 Main St",
  "role": "Developer",
  "designation": "Senior Engineer"
}`

Response:

`json
{
    "id": 11,
    "emp_id": "ffb77d766b",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "address": "123 Main St",
    "role": "Developer",
    "designation": "Senior Engineer",
    "reporting_manager": null,
    "created_by": 1,
    "created_at": "2025-08-17T18:13:51.657884Z",
    "updated_at": "2025-08-17T18:13:51.659602Z",
    "extra_data": {}
}
`
=================================success

**Update Employee**

Endpoint: PUT /api/employees/3/
Headers: Authorization: Bearer your_access_token
Request Body:

`json
{
    "role": "Senior Engineer ffrf efff"
}
`
Response:

`json
{
    "id": 11,
    "emp_id": "ffb77d766b",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "address": "123 Main St",
    "role": "Senior Engineer ffrf efff",
    "designation": "Senior Engineer",
    "reporting_manager": null,
    "created_by": 1,
    "created_at": "2025-08-17T18:13:51.657884Z",
    "updated_at": "2025-08-17T18:22:05.329734Z",
    "extra_data": {}
}`
============================success

**Delete Employee**

Endpoint: DELETE /api/employees/3/
Headers: Authorization: Bearer your_access_token
Response: Status 204 (No Content)
Action: Verify employee is removed (GET /api/employees/ should not include ID 3).

=========================================== success

Full Output Summary

Registration: Successfully creates a user.
Login: Provides a token for authenticated requests.
FormFieldAPI: Manages dynamic form fields with CRUD operations.
EmployeeAPI: Supports listing, retrieving, creating, updating, and deleting employees with search functionality.
UserAPI: Allows public registration with password validation.
_______________________________API Testing with Postman  Register a User_______________________________

**Endpoint: POST /api/register/**

**Request Body:**

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

================================

Get Form Fields

Endpoint: GET /api/form-fields/
Headers: Authorization: Bearer your_access_token
Response:
json[
    {"id": 1, "label": "Name", "field_type": "text", "order": 0, "is_required": true, "options": null},
    {"id": 2, "label": "Email", "field_type": "email", "order": 1, "is_required": true, "options": null}
]


Get All Employees

Endpoint: GET /api/employees/
Headers: Authorization: Bearer your_access_token
Response:
json[
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


Get Specific Employee

Endpoint: GET /api/employees/1/
Headers: Authorization: Bearer your_access_token
Response:
json{
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


Create New Employee

Endpoint: POST /api/employees/
Headers: Authorization: Bearer your_access_token
Request Body:
json{
    "data": {"name": "Mike Johnson"},
    "role": "Engineer",
    "designation": "Senior Engineer"
}

Response:
json{
    "id": 3,
    "emp_id": "k1l2m3n4o5",
    "data": {"name": "Mike Johnson"},
    "created_by": 1,
    "created_at": "2025-08-15T14:35:02Z",
    "updated_at": "2025-08-15T14:35:02Z",
    "role": "Engineer",
    "designation": "Senior Engineer",
    "reporting_manager": null
}


Update Employee

Endpoint: PUT /api/employees/3/
Headers: Authorization: Bearer your_access_token
Request Body:
json{
    "data": {"name": "Mike Johnson Updated"},
    "role": "Senior Engineer"
}

Response:
json{
    "id": 3,
    "emp_id": "k1l2m3n4o5",
    "data": {"name": "Mike Johnson Updated"},
    "created_by": 1,
    "created_at": "2025-08-15T14:35:02Z",
    "updated_at": "2025-08-15T14:35:03Z",
    "role": "Senior Engineer",
    "designation": "Senior Engineer",
    "reporting_manager": null
}


Delete Employee

Endpoint: DELETE /api/employees/3/
Headers: Authorization: Bearer your_access_token
Response: Status 204 (No Content)
Action: Verify employee is removed (GET /api/employees/ should not include ID 3).

Full Output Summary

Registration: Successfully creates a user.
Login: Provides a token for authenticated requests.
FormFieldAPI: Manages dynamic form fields with CRUD operations.
EmployeeAPI: Supports listing, retrieving, creating, updating, and deleting employees with search functionality.
UserAPI: Allows public registration with password validation.
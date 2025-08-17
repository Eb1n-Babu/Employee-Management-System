
Employee Management System
This is a Django-based Employee Management System with dynamic form creation, employee CRUD, and JWT authentication. Frontend uses HTML/CSS/JS with Axios for AJAX and SortableJS for drag-drop.

Features
Authentication: Login, Register, Change Password, Profile.
Form Design: Dynamic fields (text, number, date, etc.) with add/remove, drag-drop reorder.
Employee Management: Create/update using dynamic forms, list with search/filters, delete.
API: RESTful with JWT, covers all functionality.
Tech Stack: Python (Django, DRF), HTML/CSS/JS (Bootstrap, Axios, SortableJS).


To set up the employee-management-system project and create a .env file with a SECRET_KEY, follow these steps. I'll include the provided commands and add the creation of the .env file and generation of a secure SECRET_KEY.
Steps to Set Up the Project


**Clone the Repository:**
git clone https://github.com/yourusername/employee-management-system.git
`cd employee-management-system`

**Create and Activate a Virtual Environment:**

For Linux/Mac:
bash `python -m venv venv`
source venv/bin/activate`

For Windows:
bash `python -m venv venv`
venv\Scripts\activate

Install Dependencies:
bash `pip install -r requirements.txt`


**Generate a Secure Django SECRET_KEY:**
To generate a secure SECRET_KEY for your Django project, you can use Python to create a random key. Run the following command in your terminal (with the virtual environment activated):
bash `python -c "import secrets; print(secrets.token_urlsafe(50))"`
This will output a random, secure key (e.g., k9z3Xj...). Copy this key for the next step.


**Create a .env File:**
In the root directory of your project (employee-management-system), create a file named .env:
bash `touch .env  # Linux/Mac`
`echo. > .env  # Windows`

**Open the .env file in a text editor and add the SECRET_KEY:**

`SECRET_KEY=your_generated_secret_key_here`

Replace your_generated_secret_key_here with the key you copied from the previous step.
Note: If your Django project uses a library like python-decouple to load environment variables, ensure it’s installed (pip install python-decouple) and configure your settings.py to read the SECRET_KEY:

`pythonfrom decouple import config
SECRET_KEY = config('SECRET_KEY')
`

**Apply Migrations:**

bash `python manage.py makemigrations
python manage.py migrate
`

**Create a Superuser (Optional):**

Creating a superuser is not mandatory, as you noted. If you want to create one for admin access:
bash `python manage.py createsuperuser`
Follow the prompts to set up a username, email, and password.


Run the Development Server:
bash `python manage.py runserver`


**Access the Application:**
Open your browser and go to:
texthttp://127.0.0.1:8000/

**Walkthrough: Employee Management System Setup and Usage**

**Start Server:**

Activate virtual environment: source venv/bin/activate (Linux/Mac) or venv\Scripts\activate (Windows).
Run: python manage.py runserver
Access: http://127.0.0.1:8000/ (leads to login page).


**Register:**

Click "Register" on login page.
Fill in username, email, password.
Submit. Redirects to login page.


**Log In:**

Enter username/email and password.
Submit. Redirects to dashboard with:

View Employees
Add New Employee
User Profile
Change Password
Design Form Fields

**View Employees:**

Click "View Employees" on dashboard.
Shows employee list (name, email, etc.).
Note: Custom field viewing is under development; check admin panel (/admin) for details.


**Add New Employee:**

Click "Add New Employee".
Fill fields (name, email, dept, etc., including custom fields if added).
Submit. Employee added to list.


**User Profile:**

Click "User Profile".
View/edit username, email, etc.


**Change Password:**

Click "Change Password".
Enter current password, new password, confirm.
Submit. Log in again with new password.


**Design Form Fields:**

Click "Design Form Fields".
Add custom field (salary like ).
Submit. Field appears in "Add New Employee".
Note: Viewing custom fields in "View Employees" is under development.
Run python manage.py makemigrations && python manage.py migrate after adding fields, then restart server.



**Notes:**

Re-run python manage.py runserver if changes don’t reflect.
Use admin panel (/admin) for manual checks (login with superuser).
Frontend features (e.g., custom field display) are still in progress.
The JavaScript logic for dynamic field injection is directly embedded within the HTML 
and notification display is also in progress.

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
**try new username and passnword** 

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
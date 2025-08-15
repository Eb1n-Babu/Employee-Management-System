from django.urls import path
from .views import login_view, register_view, change_password_view, profile_view, form_design_view, employee_create_view, employee_list_view, employee_delete_view, FormFieldAPI, EmployeeAPI, UserAPI, TokenObtainPairView, TokenRefreshView , employee_detail_view


urlpatterns = [
    path('login/', login_view , name='login'),
    path('register/', register_view , name='register'),
    path('change-password/', change_password_view , name='change_password'),
    path('profile/', profile_view , name='profile'),
    path('form-design/', form_design_view),

    path('employee/create/', employee_create_view, name='employee_create'),
    path('employee/<int:pk>/edit/', employee_create_view, name='employee_edit'),
    path('employee/<int:pk>/', employee_detail_view, name='employee_detail'),
    path('employee/<int:pk>/delete/', employee_delete_view, name='employee_delete'),
    path('employees/', employee_list_view, name='employee_list'),

    path('api/form-fields/', FormFieldAPI.as_view()),
    path('api/employees/', EmployeeAPI.as_view()),
    path('api/employees/<int:pk>/', EmployeeAPI.as_view()),
    path('api/register/', UserAPI.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


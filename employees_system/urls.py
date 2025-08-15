from django.urls import path
from .views import login_view, register_view, change_password_view, profile_view, form_design_view, employee_create_view, employee_list_view, employee_delete_view, FormFieldAPI, EmployeeAPI, UserAPI, TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', login_view , name='login'),
    path('register/', register_view , name='register'),
    path('change-password/', change_password_view),
    path('profile/', profile_view),
    path('form-design/', form_design_view),
    path('employee/create/', employee_create_view),
    path('employee/update/<int:pk>/', employee_create_view),
    path('employee/list/', employee_list_view),
    path('employee/delete/<int:pk>/', employee_delete_view),
    path('api/form-fields/', FormFieldAPI.as_view()),
    path('api/employees/', EmployeeAPI.as_view()),
    path('api/employees/<int:pk>/', EmployeeAPI.as_view()),
    path('api/register/', UserAPI.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
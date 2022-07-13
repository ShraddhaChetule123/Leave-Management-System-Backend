from django.urls import path
from .views import *

urlpatterns = [
    path('onboard', onboard),
    path('', get_all_employee),
    path('update', update_employee),
    path('manager', get_manager),
    path('department', get_department),
    path('hardware', get_hardware),
    path('makemanager', make_manager),
    path('leave_counts', leave_counts)
]

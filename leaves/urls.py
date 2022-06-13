from django.urls import path
from .views import *

urlpatterns = [
    path('<int:request_id>', view=get_leaves),
    path('my_leaves', view=my_leaves),
    path('apply', view=request_leave),
    path('delete', view=delete_leave),
    path('update', view=update_leave),
    path('type', view=get_types),
    path('add_leave_type', view=set_types),


]


from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.UsersList.as_view(), name='users_list'),
    path('details/<int:pk>/', views.UserDetails.as_view(), name='user_details'),
]

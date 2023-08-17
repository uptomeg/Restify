from django.urls import path
from .views import *

app_name = "reservations"
urlpatterns = [
    # path('view/<int:pk>/', UserCommentView.as_view(), name='viewComment'),
    path('create/<int:pk>/', CreateReservationView.as_view(), name='createReservation'),
    path('update/<int:pk>/', UserUpdateReservationView.as_view(), name='updateReservation'),
    path('view/single/<int:pk>/', ReservationView.as_view(), name='singleReservation'),
    path('client/all/', ClientAllReservationsView.as_view(), name='clientReservations'),
    path('host/all/', HostAllReservationsView.as_view(), name='hostReservation'),
]

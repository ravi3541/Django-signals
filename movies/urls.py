from django.urls import path
from .views import (
                    ReleaseMovieAPIView,
                    MovieBookingAPIView,
                    CancelBookingAPIView)

urlpatterns = [
   path("addMovie", ReleaseMovieAPIView.as_view(), name="release-movie"),
   path("bookMovie", MovieBookingAPIView.as_view(), name="book-movie-tickets"),
   path("cancelBooking/<int:pk>/", CancelBookingAPIView.as_view(), name="cancel-movie-tickets")
]

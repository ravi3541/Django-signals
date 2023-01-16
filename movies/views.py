from movies import signals
from utilities import messages
from django.db.models import Sum
from .models import (
                    Movies,
                    MovieBooking
                    )
from rest_framework import status
from utilities.utils import ResponseInfo
from rest_framework.response import Response
from django.db.models.functions import Coalesce
from .serializers import (
                          MoviesSerializer,
                          MoviesBookingSerializer
                         )
from rest_framework.generics import (
                                     CreateAPIView,
                                     UpdateAPIView,
                                    )


class ReleaseMovieAPIView(CreateAPIView):
    """
    CLass to create api to release movie.
    """
    serializer_class = MoviesSerializer

    def __init__(self, **kwargs):
        """
        Constructor function for formatting web response.
        """
        self.response_format = ResponseInfo().response
        super(ReleaseMovieAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Post method to save movie details.
        """

        movies_serializer = self.get_serializer(data=request.data)
        if movies_serializer.is_valid(raise_exception=True):
            movies_serializer.save()
            self.response_format["status_code"] = status.HTTP_201_CREATED
            self.response_format["data"] = movies_serializer.data
            self.response_format["error"] = None
            self.response_format["messages"] = [messages.CREATION.format("Movie")]

        return Response(self.response_format)


class MovieBookingAPIView(CreateAPIView):
    """
    Class to create api to book movie tickets.
    """
    serializer_class = MoviesBookingSerializer

    def __init__(self, **kwargs):
        """
        Constructor method for formatting web response.
        """
        self.response_format = ResponseInfo().response
        super(MovieBookingAPIView).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Method to book movie tickets.
        """
        try:
            movie = Movies.objects.get(id=request.data.get("movie_id"))
            seats_occupied = MovieBooking.objects.filter(movie=movie.id, status="CONFIRMED").aggregate(sum_seats=Coalesce(Sum('seats'), 0))['sum_seats']
            seats_avail = movie.max_seats - seats_occupied
            request.data["movie"] = movie.id
            request.data["status"] = "CONFIRMED"

            booking_serializer = self.get_serializer(data=request.data)
            if booking_serializer.is_valid(raise_exception=True):
                if seats_avail >= booking_serializer.validated_data["seats"]:
                    booking_serializer.save()

                    self.response_format["status_code"] = status.HTTP_201_CREATED
                    self.response_format["data"] = booking_serializer.data
                    self.response_format["error"] = None
                    self.response_format["messages"] = [messages.CREATION.format("Booking")]
                else:
                    booking_serializer.save(status="WAITING")

                    self.response_format["status_code"] = status.HTTP_200_OK
                    self.response_format["data"] = booking_serializer.data
                    self.response_format["error"] = None
                    self.response_format["messages"] = [messages.INSUFFICIENT_SEATS.format(seats_avail)]

        except Movies.DoesNotExist:
            self.response_format["status_code"] = status.HTTP_404_NOT_FOUND
            self.response_format["data"] = None
            self.response_format["error"] = "Movie"
            self.response_format["messages"] = [messages.DOES_NOT_EXIST.format("Movie")]
        return Response(self.response_format)


class CancelBookingAPIView(UpdateAPIView):
    """
    Class to create api to cancel movie tickets.
    """
    serializer_class = MoviesBookingSerializer

    def __init__(self, **kwargs):
        """
        Constructor function for formatting web response.
        """
        self.response_format = ResponseInfo().response
        super(CancelBookingAPIView).__init__(**kwargs)

    def get_queryset(self):
        """
        Method to get queryset for booking
        """
        booking_id = self.kwargs["pk"]
        return MovieBooking.objects.filter(id=booking_id)

    def patch(self, request, *args, **kwargs):
        """
        Method to update booking status.
        """
        try:
            booking = self.get_queryset()
            booking.update(status="CANCELLED")
            signals.booking_cancelled.send(sender=self, movie=booking[0].movie)
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["data"] = "Data"
            self.response_format["error"] = None
            self.response_format["messages"] = [messages.UPDATION.format("Booking status")]

        except MovieBooking.DoesNotExist:
            self.response_format["status_code"] = status.HTTP_404_NOT_FOUND
            self.response_format["data"] = None
            self.response_format["error"] = "Booking"
            self.response_format["messages"] = [messages.DOES_NOT_EXIST.format("Booking")]

        return Response(self.response_format)

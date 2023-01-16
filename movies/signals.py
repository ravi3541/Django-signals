from django.db.models import Sum
from django.dispatch import (
                             Signal,
                             receiver
                            )
from .models import MovieBooking, Movies
from django.db.models.functions import Coalesce

booking_cancelled = Signal()


@receiver(booking_cancelled)
def promote_wait_list(sender, movie, **kwargs):
    """
    Method to promote waiting list booking.
    """
    movie = Movies.objects.get(id=movie.id)
    seats_occupied = MovieBooking.objects.filter(movie=movie.id, status="CONFIRMED").aggregate(sum_seats=Coalesce(Sum('seats'), 0))['sum_seats']

    seats_avail = movie.max_seats - seats_occupied
    waitlist = MovieBooking.objects.filter(movie=movie, status="WAITING", seats__lte=seats_avail).order_by("created_at")

    for booking in waitlist:
        if seats_avail >= booking.seats:
            booking.status = "CONFIRMED"
            booking.save()
            seats_avail -= booking.seats



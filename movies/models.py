from django.db import models


class Movies(models.Model):
    """
    Class for creating model to store movie details.
    """
    movie_name = models.CharField(max_length=20, null=False, blank=False)
    release_date = models.DateField()
    max_seats = models.IntegerField(null=False, blank=False, default=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MovieBooking(models.Model):
    """
    Class to create model to store movie booking details.
    """
    booking_status_choices = (
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
        ("WAITING", "Waiting")
    )

    movie = models.ForeignKey(Movies, null=False, blank=False, on_delete=models.CASCADE)
    seats = models.IntegerField(null=False, blank=False)
    user_name = models.CharField(max_length=20, null=False, blank=False)
    status = models.CharField(max_length=20, null=False, blank=False, choices=booking_status_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

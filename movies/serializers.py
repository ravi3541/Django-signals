from rest_framework import serializers
from .models import (
                    Movies,
                    MovieBooking
                    )


class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'


class MoviesBookingSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField()
    class Meta:
        model = MovieBooking
        fields = '__all__'
        extra_kwargs = {
            "status": {"required": False}
        }

from django.db import models

class LocationRecord(models.Model):
    email = models.EmailField()
    location_date = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField()
    lng = models.FloatField()
    city_name = models.CharField(max_length=50)
    country_name = models.CharField(max_length=50)

    class Meta:
        ordering = ['location_date']

    def __str__(self):
        return self.email + f"({self.lat}, {self.lon})"

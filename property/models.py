from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg, Max, F

#from p2.accounts.models import User
# import sys
# sys.path.insert(1, '/group_2256/P2/restify/p2/accounts')
from accounts.models import User


# Create your models here.
class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, null=False, blank=False)
    location = models.CharField(max_length=300, null=False, blank=False)
    description = models.CharField(max_length=500, null=True, blank=True)
    capacity = models.IntegerField(validators=[MinValueValidator(0)], null=False)
    room_number = models.IntegerField(validators=[MinValueValidator(0)], null=False, default=0)
    bed_number = models.IntegerField(validators=[MinValueValidator(0)], null=False, default=0)

    def is_available(self, start_date, end_date):
        overlapping_reservations = self.reservation_set.filter(
            (models.Q(start_date__range=(start_date, end_date)) | models.Q(end_date__range=(start_date, end_date)))
            | (models.Q(start_date__lte=start_date) & models.Q(end_date__gte=end_date)),
            status="approved"
        )
        return overlapping_reservations.count() == 0

    def get_latest_price(self):
        latest_period_price = self.price_set.annotate(max_start_date=Max('start_date')).filter(start_date=F('max_start_date')).first()
        if latest_period_price:
            return latest_period_price.price
        else:
            return None

    def get_average_rating(self):
        average_rating = self.propertyComment_set.aggregate(Avg('rating'))['rating__avg']
        return average_rating


class Facility(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='facility_set', null=True)
    name = models.CharField(max_length=50, null=False, blank=False)


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='image_set', null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)


class PropertyRoom(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='room_set', null=True)
    guest_capacity = models.IntegerField(validators=[MinValueValidator(0)])


class RoomBed(models.Model):
    room = models.ForeignKey(PropertyRoom, on_delete=models.CASCADE, related_name='bed_set', null=True)
    name = models.CharField(max_length=50, null=False, blank=True)
    size = models.IntegerField(validators=[MinValueValidator(0)])


class PeriodPrice(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='price_set', null=True)
    price = models.FloatField(validators=[MinValueValidator(0.0)], null=False)
    start_date = models.DateField()




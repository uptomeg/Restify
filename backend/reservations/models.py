from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models

#from p2.property.models import Property
#from p2.accounts.models import User
# import sys
# sys.path.insert(1, '/group_2256/P2/restify/p2/property')
from property.models import Property

# import sys
# sys.path.insert(1, '/group_2256/P2/restify/p2/accounts')
from accounts.models import User


# Create your models here.
class Reservation(models.Model):
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, related_name='reservation_set', null=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    status = models.CharField(max_length=50, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userReservation_set', null=True)
    price = models.FloatField(validators=[MinValueValidator(0.0)])

    def clean(self):
        super().clean()

        allowed_status_values = ['pending', 'denied', 'expired', 'approved', 'cancelled', 'terminated', 'completed', ]

        if self.status not in allowed_status_values:
            raise ValidationError(
                "Invalid status value. Allowed values are: 'pending', 'denied', 'expired', 'approved', 'cancelled', 'terminated', 'completed'.")


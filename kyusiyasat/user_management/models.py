from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from bus_management.models import Bus 

class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('driver', 'Driver'),
        ('commuter', 'Commuter'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)
    has_seen_getting_started = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if self.user_type != 'driver' and self.bus is not None:
            raise ValidationError("Only drivers can be assigned a bus.")
        super().save(*args, **kwargs)

    def get_user_type_display(self):
        """Return properly formatted user type from choices."""
        return dict(self.USER_TYPE_CHOICES).get(self.user_type, self.user_type)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
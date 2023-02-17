from django.db import models


# Create your models here.
class Hall(models.Model):
    """Hall class  """
    hall = models.CharField(max_length=255, unique=True, blank=True, null=True)
    hall_capacity = models.IntegerField(blank=True, null=True)
    projector = models.BooleanField(default=0)

    def __str__(self):
        return self.hall

class ReservationHall(models.Model):
    date = models.DateField()
    comment = models.TextField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='reservation')

    class Meta:
        unique_together = ('date', 'hall',)

    def __str__(self):
        return self.comment
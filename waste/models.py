from django.db import models
from django.contrib.auth.models import User

class Ward(models.Model):
    name = models.CharField(max_length=50, unique=True)
    total_houses = models.IntegerField()
    rate_per_house = models.FloatField(default=5)

    @property
    def total_amount(self):
        return self.total_houses * self.rate_per_house

    def _str_(self):
        return self.name
    
    
class Collection(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    ward = models.CharField(max_length=50)
    house_code = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('worker', 'ward', 'house_code', 'date')

    def _str_(self):
        return f"{self.worker.username} - {self.ward} - {self.house_code} - {self.date}"
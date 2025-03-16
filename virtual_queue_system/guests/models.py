from django.db import models

# Create your models here.
class Guest(models.Model): #CHANGE
    name         = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    walked_away  = models.BooleanField(default=False)
    removed      = models.BooleanField(default=False)
    served       = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now=True)
    guest_number = models.PositiveSmallIntegerField(null=True, blank=True)
    
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    manager  = models.ForeignKey('customers.Manager', on_delete=models.CASCADE)
    queue    = models.ForeignKey('customers.Queue', on_delete=models.CASCADE)
    category = models.ForeignKey('customers.Category', on_delete=models.CASCADE)
    operator = models.ForeignKey('customers.Operator', on_delete=models.CASCADE, null=True, blank=True)
    
    begin_of_service_time = models.DateTimeField(null=True, blank=True)
    end_of_service_time   = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.id} - {self.name}"
    

class Music(models.Model):
    song_name = models.CharField(max_length=120)
    song_url  = models.URLField(max_length=200)
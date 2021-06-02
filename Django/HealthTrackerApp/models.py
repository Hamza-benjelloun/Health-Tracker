from django.db import models

# Create your models here.
class Patient(models.Model):
    STATUS = (
            ('Sleeping','Sleeping'),
			('Falling', 'Falling'),
			('Standing', 'Standing'),
			('Sitting', 'Sitting'),
			)
    RFID= models.CharField(max_length=200,null=True)
    Firstname = models.CharField(max_length=200, null=True)
    Lastname= models.CharField(max_length=200, null=True)
    Cin = models.CharField(max_length=200, null=True)
    State = models.CharField(max_length=200,choices=STATUS,default=STATUS[0][0])
    Temperature = models.CharField(max_length=200,null=True)
    Tension = models.CharField(max_length=200,null=True)
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.Lastname
class measures(models.Model):
    tension_state = models.CharField(max_length=200,null=True)
    tension = models.CharField(max_length=200,null=True)
    temp_state = models.CharField(max_length=200,null=True)
    temperature = models.CharField(max_length=200,null=True)
    id_patient = models.CharField(max_length=200,null=True)    
    date_time = models.DateTimeField(auto_now_add=True)
class state(models.Model):
    id_patient = models.CharField(max_length=200, null=True)
    status= models.CharField(max_length=200, null=True)
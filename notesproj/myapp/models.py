from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Login(models.Model):
 logid=models.AutoField(primary_key=True)
 username=models.TextField(max_length=30,default='')
 name=models.TextField(max_length=20)
 email=models.TextField(max_length=50)
 password=models.TextField(max_length=20)





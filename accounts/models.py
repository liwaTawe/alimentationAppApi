from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    PRODUCER = "PRODUCER"
    CLIENT = "CLIENT"
    ADMIN = "ADMIN"

    ROLE_CHOICES = (
        (PRODUCER, "Producer"),
        (CLIENT, "Client"),
        (ADMIN, "Admin")
    )

    role = models.CharField(max_length=100, choices= ROLE_CHOICES, verbose_name= "Rôle")



class Client(User):
    pass 


class Producer(User):
    pass 


class Admin(User):
    pass

from django.db import models

class TechnicianProfession(models.TextChoices):
    PLUMBER = "plumber", "Plumber"
    ELECTRICIAN = "electrician", "Electrician"
    CARPENTER = "carpenter", "Carpenter"
    MECHANIC = "mechanic", "Mechanic"
    PAINTER = "painter", "Painter"
    GARDENER = "gardener", "Gardener"
    CLEANER = "cleaner", "Cleaner"
    LOCKSMITH = "locksmith", "Locksmith"
    OTHER = "other", "Other"

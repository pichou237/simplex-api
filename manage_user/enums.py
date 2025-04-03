from django.db import models

class TechnicianStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"

class TechnicianProfession(models.TextChoices):
    PLUMBER = "plumber", "Plumber"
    ELECTRICIAN = "electrician", "Electrician"
    CARPENTER = "carpenter", "Carpenter"
    MECHANIC = "mechanic", "Mechanic"
    OTHER = "other", "Other"

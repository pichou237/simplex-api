from django.db import models

class TechnicianProfession(models.TextChoices):
    PLUMBER = "plumber", "Plumber"
    ELECTRICIAN = "electrician", "Electrician"
    CARPENTER = "carpenter", "Carpenter"
    MECHANICIAN = "mechanician", "Mechanician"
    PAINTER = "painter", "Painter"
    GARDENER = "gardener", "Gardener"
    CLEANER = "cleaner", "Cleaner"
    LOCKSMITH = "locksmith", "Locksmith"
    ROOFER = "roofer", "Roofer"
    HVAC = "hvac", "HVAC Technician"
    WELDER = "welder", "Welder"
    MASON = "mason", "Mason"
    LANDSCAPER = "landscaper", "Landscaper"
    PLASTERER = "plasterer", "Plasterer"
    OTHER = "other", "Other"

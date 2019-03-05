from django.db import models

# Create your models here.
class Lawyer(models.Model):
    name = models.CharField(max_length=255, blank=True, default='')
    job_title = models.CharField(max_length=255, blank=True, default='')
    key_practice_areas = models.CharField(max_length=255, blank=True, default='')
    law_prac_name = models.CharField(max_length=255, blank=True, default='')
    admission_date = models.DateField(default=None, blank=True, null=True)
    law_prac_type = models.CharField(max_length=255, blank=True, default='')
    email = models.EmailField(max_length=70, blank=True, default='')
    website = models.CharField(max_length=255, blank=True, default='')
    tel = models.CharField(max_length=20, blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    cases = models.CharField(max_length=1000, blank=True, default='')
    disciplinary_fault = models.BooleanField(default=False)

from django.db import models
from django.conf import settings
from django.utils import timezone

CONTRACT = (
    ('Part Time', 'Part Time'),
    ('Full Time', 'Full Time'),
    ('Freelance', 'Freelance'),
)

LOCATION = (
    ('Mumbai','Mumbai'),
    ('Bangalore','Bangalore'),
    ('Pune','Pune'),
    ('Nashik','Nashik'),
    ('Remote','Remote'),
)

class Job(models.Model):

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    location = models.CharField(choices=LOCATION, max_length=50)
    description = models.TextField(blank=True)
    about = models.TextField(blank=True)
    job_date = models.DateTimeField(default=timezone.now, blank=True)
    contract = models.CharField(choices=CONTRACT, max_length=150)
    is_published = models.BooleanField(default=True)
    vacancy = models.CharField(max_length=10, null=True, blank=True)
    experience = models.CharField(max_length=100, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    deadline = models.DateTimeField()
    main_image = models.ImageField(upload_to='photos/%Y/%m%d/', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-job_date']
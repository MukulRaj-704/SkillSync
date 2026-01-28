from django.db import models
from django.conf import settings

class Job(models.Model):
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=120, blank=True)
    description = models.TextField()
    salary = models.CharField(max_length=100, blank=True)

    is_active = models.BooleanField(default=True)   # ✅ NEW

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
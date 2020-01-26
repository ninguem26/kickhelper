from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    currency = models.CharField(max_length=200)
    expected_launch = models.DateField()
    deadline = models.DateField()
    goal = models.FloatField()
    current_state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
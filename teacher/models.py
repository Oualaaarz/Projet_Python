from django.db import models
from department.models import Department

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.ForeignKey(
    Department,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    def __str__(self):
        return self.name

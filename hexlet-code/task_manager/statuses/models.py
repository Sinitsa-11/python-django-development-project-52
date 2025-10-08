from django.db import models


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        "user.CustomUser",
        editable=False,
        on_delete=models.CASCADE,
        related_name='status_related_author'
    )

    def __str__(self):
        return self.name

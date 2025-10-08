from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.ForeignKey(
        "statuses.Status",
        on_delete=models.CASCADE,
        related_name='task_related_status'
    )
    label = models.ForeignKey(
        "label.Label",
        on_delete=models.CASCADE,
        related_name='task_related_label'
    )
    user = models.ForeignKey(
        "user.CustomUser",
        on_delete=models.CASCADE,
        related_name='task_related_user'
    )
    author = models.ForeignKey(
        "user.CustomUser",
        editable=False,
        on_delete=models.CASCADE,
        related_name='task_related_author'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

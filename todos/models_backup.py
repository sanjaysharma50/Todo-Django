from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Todo(models.Model):

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    CATEGORY_CHOICES = [
        ('work', 'Work'),
        ('study', 'Study'),
        ('personal', 'Personal'),
        ('shopping', 'Shopping'),
        ('ideas', 'Ideas'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='todos',
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    completed = models.BooleanField(
        default=False
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )

    due_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def is_overdue(self):
        """
        Returns True when the task has a due date,
        is not completed, and the due date has passed.
        """

        if self.completed:
            return False

        if not self.due_date:
            return False

        return self.due_date < timezone.localdate()

    def __str__(self):
        return self.title
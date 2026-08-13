from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'user',
        'priority',
        'completed',
        'due_date',
        'created_at',
    )

    list_filter = (
        'priority',
        'completed',
        'due_date',
    )

    search_fields = (
        'title',
        'description',
        'user__username',
        'user__email',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 25
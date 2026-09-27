from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo

        fields = [
            'title',
            'description',
            'priority',
            'category',
            'due_date',
            'recurrence',
            'recurrence_until',
            'reminder_at',
        ]

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter task title',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Enter task description',
                    'rows': 4,
                }
            ),

            'priority': forms.Select(),

            'category': forms.Select(),

            'due_date': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),

            'recurrence': forms.Select(),

            'recurrence_until': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),

            'reminder_at': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        recurrence = cleaned_data.get('recurrence')
        due_date = cleaned_data.get('due_date')
        recurrence_until = cleaned_data.get(
            'recurrence_until'
        )

        if recurrence != 'none' and not due_date:

            self.add_error(
                'due_date',
                'Recurring task ke liye Due Date required hai.'
            )

        if (
            recurrence_until
            and due_date
            and recurrence_until < due_date
        ):

            self.add_error(
                'recurrence_until',
                'Repeat Until date Due Date ke baad honi chahiye.'
            )

        return cleaned_data
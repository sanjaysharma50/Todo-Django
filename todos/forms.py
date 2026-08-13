from django import forms

from .models import Todo


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo

        fields = [
            'title',
            'description',
            'priority',
            'due_date',
        ]

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter task title'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Enter task description',
                    'rows': 4
                }
            ),

            'due_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
        }
        
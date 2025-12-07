from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text='Comma-separated tags')

    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'tags']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['tags'].initial = ', '.join(t.name for t in instance.tags.all())

from django.forms import ModelForm, ModelChoiceField, ChoiceField
from .models import Task
from .. import statuses


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

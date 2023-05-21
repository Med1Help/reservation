from django.forms import ModelForm
from .models import User, Event

class UserForm(ModelForm):
    class Meta:
        model  = User
        fields = ['name','password','email','num','role']

class EventForm(ModelForm):
    class Meta:
        model   = Event
        fields  = '__all__'
        exclude = ['owner']
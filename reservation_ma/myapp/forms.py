from django.forms import ModelForm
from .models import User, Event, TicketRef

class UserForm(ModelForm):
    class Meta:
        model  = User
        fields = ['name','password','email','num','role']

class EventForm(ModelForm):
    class Meta:
        model   = Event
        fields  = '__all__'
        exclude = ['owner']

class TicketRefForm(ModelForm):
    class Meta:
        model   = TicketRef
        fields  = '__all__'
        exclude = ['event']     
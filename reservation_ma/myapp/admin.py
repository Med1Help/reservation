from django.contrib import admin
from .models import User , Event , Client , Ticket , TicketRef , Order

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Client)
admin.site.register(Ticket)
admin.site.register(TicketRef)
admin.site.register(Order)
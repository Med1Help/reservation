from django.urls import path
from . import views

urlpatterns = [
    path('home',views.home,name='home'),
    # path('test',views.test,name='test'),
    path('client-form',views.order_validation,name='client-form'),
    path('get-ticket',views.getTicket,name='get-ticket'),
    path('ticket-form',views.ticketForm,name='ticket-form'),
    path('managers-dash',views.managers,name='managers-dash'),
    path('manager-form',views.addManager_form,name='manager-form'),
    path('manager_update-form/<str:idManager>',views.updateManager,name='manager_update-form'),
    path('manager-delete/<str:idManager>',views.deleteManager,name='manager-delete'),
    path('event-dash/<str:idManager>',views.events,name='event-dash'),
    path('event-add/<str:idManager>',views.addEvent_form,name='event-add'),
    path('event-update/<str:idManager>/<str:idEvent>',views.updateEvent,name='event-update'),
    path('event-delete/<str:idManager>/<str:idEvent>',views.deleteEvent,name='event-delete'),
    path('user-login',views.userLogin,name='user-login'),
    path('user-logout',views.userLogout,name='user-logout'),
]
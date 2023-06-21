from django.shortcuts import render , redirect
from .models import Event , TicketRef , Ticket , Client , Order , User
from .forms import TicketRefForm, UserForm, EventForm
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.template.defaulttags import register

def home(req):
    q = req.GET.get('q')
    if q is not None:
        events    = Event.objects.filter(
            Q( title__icontains =q )
            )
    else:
        events    = Event.objects.all()
    ticketRef = TicketRef.objects.all() 
    context   = {'events':events,'tickets':ticketRef}
    return render(req,'myapp/home.html',context)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@login_required(login_url='user-login')
def events(req,idManager):
    events    = Event.objects.filter(owner_id=idManager)
    ticketRef = TicketRef.objects.all()
    tickets   = {}
    for event in events:
        for ticket in ticketRef:
            if (ticket.event == event):
                if event.id in tickets:
                    tickets[event.id].append(ticket)
                else:
                    tickets[event.id] = [ticket]  
    print("tickets length ",tickets)
    context   = {'events':events,'tickets':tickets}
    return render(req,'myapp/events_dash.html',context)

@login_required(login_url='user-login')
def addEvent_form(req,idManager):
    form = EventForm()
    if req.method == 'POST':
        form = EventForm(req.POST,req.FILES)
        if form.is_valid():
            event       = form.save(commit=False)
            manager     = User.objects.get(id=idManager)
            event.owner = manager
            print(event,manager)
            event.save()
            return redirect('ticketref',idManager,event.id)  
        else:
            print("what is wrong ??? ",form)    
    context = {'form' : form}
    return render(req,'myapp/event_form.html',context)

#TicketRefForm
@login_required(login_url='user-login')
def addTicketRef_form(req,idManager,idEvent):
    form = TicketRefForm()
    if req.method == 'POST':
        form = TicketRefForm(req.POST)
        if form.is_valid():
            ticketRef       = form.save(commit=False)
            ticketRef.event = Event.objects.get(id=idEvent)
            ticketRef.save()
            return redirect('event-dash',idManager)  
        else:
            print("what is wrong ??? ",form)    
    context = {'form' : form , 'idEvent':idEvent}
    return render(req,'myapp/TicketRef_form.html',context)


@login_required(login_url='user-login')
def updateEvent(req,idEvent,idManager):
    event   = Event.objects.get(id=idEvent)
    form    = EventForm(instance=event)
    if req.method == 'POST':
        form = EventForm(req.POST,req.FILES,instance=event)
        if form.is_valid():
            event       = form.save(commit=False)
            manager     = User.objects.get(id=idManager)
            event.owner = manager
            form.save()
        return redirect('event-dash',idManager)       
    context = {'form' : form}
    return render(req,'myapp/event_form.html',context)

@login_required(login_url='user-login')
def deleteEvent(req,idEvent,idManager):
    event = Event.objects.get(id=idEvent)
    event.delete()
    return redirect('event-dash',idManager) 
     
@login_required(login_url='user-login')
def managers(req):
    ticketRef = TicketRef.objects.all() 
    managers = []
    if req.user.role == 'manager':
        events    = Event.objects.filter(owner=req.user.id)
    else:
        events    = Event.objects.all()
        managers = User.objects.all()
        events    = Event.objects.all()
    tickets   = {}
    for event in events:
        for ticket in ticketRef:
            if (ticket.event == event):
                if event.id in tickets:
                    tickets[event.id].append(ticket)
                else:
                    tickets[event.id] = [ticket]  
    print("tickets length managers",tickets)
    context  = {'managers' : managers,'events':events,'tickets':tickets}
    return render(req,'myapp/managers_dash.html',context)

@login_required(login_url='user-login')
def addManager_form(req):
    form = UserForm()
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            user          = form.save(commit=False)
            user.role     = 'manager'
            user.password = make_password(user.password)
            user.save()
            login(req,user)
            return redirect('managers-dash') 
        else:
                messages.error(req,'You have an issue ')     
    context = {'form' : form}
    return render(req,'myapp/manager_form.html',context)

@login_required(login_url='user-login')
def updateManager(req,idManager):
    manager = User.objects.get(id=idManager)
    form    = UserForm(instance=manager)
    if req.method == 'POST':
        form = UserForm(req.POST,instance=manager)
        if form.is_valid():
            form.save()
        return redirect('managers-dash')       
    context = {'form' : form}
    return render(req,'myapp/manager_form.html',context)

@login_required(login_url='user-login')
def deleteManager(req,idManager):
    manager = User.objects.get(id=idManager)
    manager.delete()
    return redirect('managers-dash') 

@login_required(login_url='user-login')     
def dashbord(req):
    print("user role : ",req.user.role)
    if(req.user.role == 'manager'):
      return redirect('event-dash',req.user.id) 
    if(req.user.role == 'admin'):
      return redirect('managers-dash')    

def ticketForm(req):
    event   = req.GET.get('ev')
    context = {'ticket_types':["prime","ordinary"],'event':event}
    return render(req,'myapp/ticket_fomr.html',context)


def getTicket(req):
    if req.method == 'GET':
        eventTitle = req.GET.get('ev')
        tickType   = req.GET.get('ticket_type')
        number     = int(req.GET.get('number'))
        tcheck     = verifying_ticket_dispo(eventTitle,tickType,number)
        if tcheck != False:
            context    = {'ev':eventTitle,'ticket_type':tickType,'number':number , 'price' : tcheck['price']}
            return render(req,'myapp/client_form.html',context)
        else:
            home(req)
    elif req.method == 'POST':
            eventTitle = req.POST.get('ev')
            tickType   = req.POST.get('tck')
            number     = int(req.POST.get('n'))
            name       = req.POST.get('name')
            email      = req.POST.get('email')
            cardNumber = req.POST.get('cardNumber')
            cvv        = req.POST.get('cvv')
            exp        = req.POST.get('exp')
            print(eventTitle," ",tickType," ",number)
            ticketref  = verifying_ticket_dispo(eventTitle,tickType,number)
            if( ticketref == False): return home(req)
            ticketref['ticketref'].ticketDispo = ticketref['ticketref'].ticketDispo - number
            ticketref['ticketref'].save()
            client = Client(name=name, email=email, cardNumber=cardNumber, cvv=cvv, exp=exp)
            client.save()
            for i in range(number) :
                ticket = Ticket(event=ticketref['ticketref'].event, price=ticketref['ticketref'].price, ticketType=ticketref['ticketref'].ticketType, date=ticketref['ticketref'].event.date,  time=ticketref['ticketref'].event.time, ref=ticketref['ticketref'].event.title)
                ticket.save()
                order  = Order(client=client, ticket=ticket)
                order.save()
                print("n° : ",i,client,ticket,order) 
            return home(req)

def verifying_ticket_dispo (eventTitle,tickType,number):
    ticketrefL = TicketRef.objects.filter(
        Q(event__title = eventTitle) &
        Q(ticketType__exact = tickType)   &
        Q(ticketDispo__gte = number)
    )
    if len(ticketrefL) != 0 :
        ticketref = ticketrefL[0]
        totalPrice = ticketref.price * number 
        print('good ** verifying_ticket_dispo ',ticketref,totalPrice )
        return {'ticketref':ticketref,'price':totalPrice}
    else:
        print('bad ** verifying_ticket_dispo')    
        return False

def order_validation(req):
    return render(req,'myapp/client_form.html')


def userLogin(req):
    context = {}
    if req.method == 'POST':
        email = req.POST.get('email')
        pwd = req.POST.get('password')
        try:
            user = User.objects.get(email=email)
            print('first retrive passed',user)
        except:
            messages.error(req,'Username uncorrect')  
            return redirect('home')  
        
        user = authenticate(req,username=email,password=pwd)
        print(make_password(pwd))
        if user is not None:
                login(req,user)
                messages.error(req,'Loged in succesfuly')
                return redirect('home')
        else:
            messages.error(req,'password incorrect')
        
    return render(req,'myapp/login_form.html',context)

def userLogout(req):
    logout(req)
    return redirect('home')
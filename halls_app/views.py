from datetime import date

from django.db import ProgrammingError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from halls_app.models import Hall, ReservationHall
from .forms import HallForm, HallNameForm, HallCapacityForm, ProjectorForm, ReserveForm


# Create your views here.
def add_hall(request):
    """ View for adding new entry to database if input is valid"""
    if request.method == "GET":
        form = HallForm()
        return render(request, 'add_hall.html', context={'form': form})

    if request.method == "POST":
        form = HallForm(request.POST)
        if form.is_valid():
            hall_name = form.cleaned_data['hall']
            hall_cap = form.cleaned_data['hall_capacity']
            projector = form.cleaned_data['projector']

            if hall_cap < 0:
                return HttpResponse("Pojemność sali nie może być ujemna")
            hall_objects = Hall.objects.filter(hall=hall_name)
            if hall_objects:
                return HttpResponse("Ta sala już istnieje")
            else:
                Hall.objects.create(
                    hall=hall_name,
                    hall_capacity=hall_cap,
                    projector=projector
                )
                return redirect('/room/home/')

        else:
            return HttpResponse("Nie podano nazwy sali")


def show_all(request):
    show_all = Hall.objects.all()
    today = date.today()

    try:
        ReservationHall.objects.get(date=today)
        reservation = 1
    except ReservationHall.DoesNotExist:
        reservation = 0
    return render(request, 'show_all.html', context={'show_all': show_all, 'reservation': reservation})


def show_hall(request, hall_id):
    """View for requesting information on one specific hall by its id """
    if request.method == 'GET':
        hall = Hall.objects.get(id=hall_id)
        reservations = ReservationHall.objects.filter(hall=hall_id).order_by('id')
        return render(request, 'show_hall.html', context={
            'hall': hall,
            'reservations': reservations
        })


def hall_remove(request, hall_id):
    """View for removing specific hall from database"""
    if request.method == 'GET':
        Hall.objects.filter(id=hall_id).delete()
        show_all = Hall.objects.all()
        return render(request, 'show_all.html', context={'show_all': show_all})


def modify_hall(request, hall_id):
    """View for modifying specific hall in database"""
    if request.method == "GET":
        hall = Hall.objects.get(id=hall_id)
        name = HallNameForm()
        capacity = HallCapacityForm()
        projector = ProjectorForm()
        context = {
            'hall': hall,
            'name': name,
            'capacity': capacity,
            'projector': projector
        }
        return render(request, 'modify.html', context=context)
    elif request.method == "POST":
        hall = Hall.objects.get(id=hall_id)
        name = HallNameForm(request.POST)
        capacity = HallCapacityForm(request.POST)
        project = ProjectorForm(request.POST)
        if name.is_valid():
            hall_name = name.cleaned_data['hall']
            if len(Hall.objects.filter(hall=hall_name)) > 1:
                return HttpResponse("Ta Nazwa sali jest już zajęta")
            else:
                hall.hall = name.cleaned_data['hall']
                hall.save()
        if capacity.is_valid():
            cap = capacity.cleaned_data['hall_capacity']
            if cap < 0:
                return HttpResponse("Pojemność sali nie może być ujemna")
            else:
                hall.hall_capacity = capacity.cleaned_data['hall_capacity']
        if project.is_valid():
            hall.projector = project.cleaned_data['projector']
        return redirect('/room/home/')

    else:
        return HttpResponse("Nie podano nazwy sali")


def reserve_hall(request, hall_id):
    """View for reserving Hall"""
    if request.method == 'GET':
        form = ReserveForm()
        hall = Hall.objects.get(id=hall_id)
        reservations = ReservationHall.objects.filter(hall=hall_id).order_by('id')
        return render(request, 'reserve_hall.html', context={
            'form': form,
            'hall': hall,
            'reservations':reservations})

    elif request.method == 'POST':
        form = ReserveForm(request.POST)
        hall = Hall.objects.get(id=hall_id)
        if form.is_valid():
            reservation_date = form.cleaned_data['date']
            reservation_comment = form.cleaned_data['comment']
            try:
                reservations = ReservationHall.objects.filter(hall=hall_id)
                for reservation in reservations:
                    print(date.today(), '==', reservation_date)
                    if reservation.date == reservation_date:
                        return HttpResponse('Sala jest zarezerwowana tego dnia')
                    elif date.today() > reservation_date:
                        return HttpResponse('Niepoprawna data')
                    else:
                        pass
            except ProgrammingError:
                pass
            new_reservation = ReservationHall()
            new_reservation.date = reservation_date
            new_reservation.comment = reservation_comment
            new_reservation.hall = hall
            new_reservation.save()
            return redirect('/room/home')
        print(form.errors.as_data())
        return HttpResponse("To Formularz jest zły")
    return HttpResponse("To nie post i nie Get")

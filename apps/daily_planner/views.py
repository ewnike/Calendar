# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from . models import *
from django.db.models import Count
from datetime import datetime
from datetime import timedelta
import re
EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your views here.
def index(request):
    context = {}
    if 'invalid_login' in request.session:
        request.session.pop('invalid_login')
        context['login_messages'] = True
    elif 'invalid_registration' in request.session:
        request.session.pop('invalid_registration')
        context['registration_messages'] = True


    return render(request, 'daily_planner/index.html', context)


def register(request):
    if request.method == 'POST':
        isValid=True
        if len(request.POST['first_name']) < 1:
            messages.add_message(request, messages.ERROR, "Please enter your first name.")
            isValid = False
        elif not request.POST['first_name'].isalpha():
            messages.add_message(request, messages.ERROR,"Please enter a valid first name.")
            isValid = False

        if len(request.POST['last_name']) < 1:
            messages.add_message(request, messages.ERROR, "Please enter your last name.")
            isValid = False
        elif not request.POST['last_name'].isalpha():
            messages.add_message(request, messages.ERROR,"Please enter a valid last name.")
            isValid = False

        if len(request.POST['email']) < 1:
            messages.add_message(request, messages.ERROR, "Please enter a valid email.")
            isValid = False
        elif not EMAIL_REGEX.match(request.POST['email']):
            messages.add_message(request, messages.ERROR, "Invalid Email. Please Re-Enter! ")
            isValid = False

        if len(request.POST['password']) < 9:
            messages.add_message(request, messages.ERROR, "Password must be longer than 8 characters.")
            isValid = False
        elif request.POST['password'] != request.POST['confirm_password']:
            messages.add_message(request, messages.ERROR, "Password and Confirm do not match!")
            isValid = False

        if not isValid:
            request.session['invalid_registration'] = True
            return redirect('/')
        else:
            new_user = Users.objects.create(first_name=request.POST['first_name'],aka=request.POST['aka'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'], birthdate=request.POST['birthdate'])
            request.session['first_name']=new_user.first_name
            request.session['email']=new_user.email
            return redirect('daily_planner:home')

def login(request):
    if request.method == "POST":
        try:
            user = Users.objects.get(email=request.POST['email'])
            request.session['email'] = request.POST['email']

            if user.password==request.POST['password']:
                request.session['first_name'] = user.first_name
                return redirect ('daily_planner:home')
            else:
                request.session['invalid_login'] = True
                messages.add_message(request, messages.ERROR,"Password is invalid.")
                return redirect('/')
        except:
            request.session['invalid_login'] = True
            messages.add_message(request, messages.ERROR,"That email is not registered!")
            return redirect('/')

def homepage(request):
    user=Users.objects.filter(email=request.session['email'])
    for u in user:
        id = user
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    appointments =Appointments.objects.all()
    expired_appts = Appointments.objects.filter(user_id=u.id).filter(time__lt=today).order_by('time'),
    today_appts =Appointments.objects.filter(user_id=u.id).filter(time__range=[today, tomorrow.date()]).order_by('time'),
    future_appts =Appointments.objects.filter(user_id=u.id).filter(time__gt=tomorrow.date()).order_by('time')
    context={
        'user': user,
        'first_name':request.session['first_name'],
        'appointments':appointments,
        'today':today,
        'expired_appts':expired_appts,
        'today_appts':today_appts,
        'future_appts':future_appts
        }
    print context['today_appts']
    return render(request, 'daily_planner/homepage.html', context)



def add_appointment(request):
    if request.method == "POST":
        errors = "false"
        datetimevar = request.POST['date'] + str(" ") + str(request.POST['time'])
        print "concat date and time value is ", datetimevar
        today = datetime.now()

        if len(request.POST['task']) < 1:
            messages.error(request, "please enter a name for your appointment in task")
            errors = "true"
        if str(today) > datetimevar:
            print "You entered an invalid date/time, please re-enter."
            messages.error(request, 'Please enter a valid appointment date/time')
            errors = "true"
        if len(request.POST['time']) < 5:
            messages.error(request, 'please enter a valid time for your appointment')
            errors = "true"
        if errors == "true":
            return redirect('daily_planner:add_appointment')
        else:
            print "that is a valid date and time you entered!"
            Appointments.objects.create(task=request.POST['task'], time=datetimevar, status="Pending", user_id = Users.objects.get(first_name=request.session['first_name']).id)

    return redirect('daily_planner:homepage')

def edit_appointment(request, id):
    edit = Appointments.objects.get(id = id)

    # for e in edit:
    year = edit.time
    print "match this", year
    month = year.month
    if month < 10:
        month = str(0) + str(month)
    day = year.day
    if day < 10:
        day = str(0) + str(day)
    hour = year.hour
    if hour < 10:
        hour = str(0) + str(hour)
    minute = year.minute
    if minute < 10:
        minute = str(0) + str(minute)

    madedate = str(year.year) + "-" + str(month) + "-" + str(day)
    madetime = str(hour) + ":" + str(minute)

    context = {'edit': edit, 'madedate': madedate, 'madetime': madetime}

    return render(request,"daily_planner/edit_appointment.html", context)

def update_appointment(request, id):
    if request.method =="POST":
        newtime = request.POST['date'] + str(" ") + str(request.POST['time'])
        errors = "false"
        rightnow = datetime.now()


        if len(request.POST['task']) < 1:
            messages.error(request, "please enter a name for your appointment in task")
            errors = "true"
            return redirect('/edit_appointment/'+id)
        if request.POST['status'] != "Pending":
            Appointments.objects.filter(id=id).update(task=request.POST['task'], status=request.POST['status'])
            return redirect('/homepage')
        if newtime < str(rightnow):
            messages.error(request, 'Please enter a valid appointment date/time')
            errors = "true"
        if errors == "true":
            return redirect('/edit_appointment/'+id)
        print request.POST['task'], request.POST['status']

        Appointments.objects.filter(id=id).update(task=request.POST['task'], status=request.POST['status'], time = newtime)

    return redirect('/homepage')


def delete_appointment(request, id):
    Appointments.objects.filter(id=id).delete()
    return redirect ('daily_planner:homepage')

def logout(request):
    request.session.clear()
    return redirect('/')

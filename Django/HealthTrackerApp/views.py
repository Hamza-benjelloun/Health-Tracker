from typing import Optional
from HealthTrackerApp.models import *
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import PatientForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('tracker')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('tracker')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request,'HealthTrackerApp/index.html',context)
@login_required(login_url='home')
def track(request,pid=None):    
    openmodal=None
    if(pid is None):
        form = PatientForm()
    else:
        openmodal="openmodal"
        Patient1 = Patient.objects.get(RFID=pid)
        form = PatientForm(instance=Patient1)
    if request.method=='POST':
        if(pid is None):
            form = PatientForm(request.POST)
        else:
            form = PatientForm(request.POST, instance=Patient1)
        if form.is_valid():
          	form.save()
          	return redirect('home')
    measure=[]
    temperatures=[]
    tensions=[]
    states=[]
    tabmeasures={}
    patients = Patient.objects.all()
    for i in patients:
        if i.RFID is not None:
            # a=measures()
            # a.id_patient=i.RFID
            # a.save()
            # b=state()
            # b.id_patient=i.RFID
            # b.save()
            measure_t=measures.objects.filter(id_patient=i.RFID)
            measure_s=state.objects.filter(id_patient=i.RFID)
            measure =measures.objects.filter(id_patient=i.RFID).latest("date_time")
            	
            if(measure_t is not None):
                i.Temperature=measure_t.latest("date_time").temperature
                i.Tension=measure_t.latest("date_time").tension
                for j in range(len(measure_t)) :
                    temperatures.append(measure_t[j].temperature)
                print(temperatures)
                for j in range(len(measure_t)) :
                    tensions.append(measure_t[j].tension)
                print(tensions)
            else :
                i.Temperature=None
                i.Tension=None
                temperatures.append(None)
                tensions.append(None)
            if(measure_s is not None):
                    i.State=measure_s.latest("id").status
                    for j in range(len(measure_s)) :
                        states.append(measure_s[j].status)
                    print(states)
            else:
                i.State="Sleeping"
                states.append("Sleeping")
            tabmeasures[i.id]=[temperatures,tensions,states]
            print(tabmeasures)
            i.save()
    context = {'form':form,'patients':patients,'openmodal':openmodal,'tabmeasures':tabmeasures}	
    return render(request,'HealthTrackerApp/Tracker.html',context)
def logoutUser(request):
	logout(request)
	return redirect('home')
# def updatePatient(request, pid):
# 	Patient = Patient.objects.get(id=pid)
# 	form = PatientForm(instance=Patient)
# 	if request.method == 'POST':
# 		form = PatientForm(request.POST, instance=Patient)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('/')
# 	context = {'form':form}
# 	return render(request, 'HealthTrackerApp/Tracker.html', context)
@login_required(login_url='home')
def deletePatient(request, pid):
	Patient1 = Patient.objects.get(Cin=pid)
	Patient1.delete()
	return redirect('/')
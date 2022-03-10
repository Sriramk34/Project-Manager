from asyncio.windows_events import NULL
from pickle import NONE
from pydoc import isdata
from django.forms import NullBooleanField
from django.http import HttpResponse, HttpResponseRedirect, response
from django.shortcuts import render
from .models import Projects, Users, login, assignments
from django.db.models import Q 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def checklogin(request):
    try:
        if request.session["_auth_user_id"] != NULL:
            return 1
        else:
            return 0
    except:
        return 0


def empty(request):
    if checklogin(request) == 1:
        return HttpResponseRedirect("/index/")
    else:
        return HttpResponseRedirect("/login/")


def index(request):
    if checklogin(request) == 1:
        return render(request, 'main/index.html',{
        "emp":Users.objects.get(user = User.objects.get(id = request.session["_auth_user_id"]))
         })
    else:
        return HttpResponseRedirect("/login/")  
    

def manage(request):                                                            
    if checklogin(request) != 1:
        return HttpResponseRedirect("/login/")
    projects = Projects.objects.filter(~Q(status = "C"))
    employees = Users.objects.filter(CurrentlyWorking = True)
    if Users.objects.get(user = User.objects.get(id = request.session["_auth_user_id"])).role == "Manager":
        return render(request, 'main/manage.html',{
            "projects": projects,
            "employees": employees
        })
    else:
        return HttpResponseRedirect("/index/")


def login_site(request):
    if checklogin(request) == 1:
        logout(request)
        return render(request, 'main/login.html')

    if request.method == 'POST':
        usern = str(request.POST['username'])
        pwd = str(request.POST['password'])
        user = authenticate(username = usern, password = pwd)
        if user is not None:
            login(request, user)
            #print(request.session["_auth_user_id"])
        else:
            return HttpResponse("<h2>Please Check your Username or Password</h2>")
        return HttpResponseRedirect("/index/")
    else:
        return render(request, 'main/login.html')


def assigned_tasks(request):                                            #Views function for assigned tasks page
    if checklogin(request) != 1:
        return HttpResponseRedirect("/login/")
    user = Users.objects.get(user = User.objects.get(id = request.session["_auth_user_id"]))   
    tasks = assignments.objects.filter(asignee = user)
    #print(tasks)
    return render(request, "main/assigned.html",{
        "tasks" : tasks,
    })


def progress(request):
    if not checklogin(request):
        return HttpResponseRedirect("/login/")

    statuses ={
        "H":"On Hold",
        'F':"Finished",
        'C':"Confirmed",
        'P':"In Progress"
    }

    if(request.method == "POST"):
        req = None
        try:
            wd = int(float(request.POST['wd']))
            id = int(request.POST['ID'])
            st = str(request.POST['status'])
            req = 'update'
        except:
            try:
                saves = str(request.POST['Saves'])
                if saves == "True":
                    req = 'save'
            except:
                print("Error")
                return HttpResponseRedirect("/progress/")

        if req == "update":
            assgn = assignments.objects.get(id = id)
            assgn.work_done_temp = wd
            assgn.assignment_status = st
            print(st)
            assgn.save()
        elif req == "save":
            user = Users.objects.get(user = User.objects.get(id = request.session["_auth_user_id"]))
            assgn = assignments.objects.filter(~Q(assignment_status="V"), asignee = user)
            for x in assgn:
                x.work_done = x.work_done + x.work_done_temp
                x.work_done_temp = 0
                x.save()

    user = Users.objects.get(user = User.objects.get(id = request.session["_auth_user_id"]))   
    tasks = assignments.objects.filter(~Q(assignment_status="V"), asignee = user)
    return render(request, "main/progress.html",{
        "tasks": tasks,
        "statuses":[('H',"On Hold"), ('F',"Finished"), ('C',"Confirmed"), ('P',"In Progress")],
    })
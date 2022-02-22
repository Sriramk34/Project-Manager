from asyncio.windows_events import NULL
from pydoc import isdata
from django.forms import NullBooleanField
from django.http import HttpResponse, HttpResponseRedirect, response
from django.shortcuts import render
from .models import Projects, Users, login, assignments
from django.db.models import Q 

def checklogin(request):
    try:
        if request.session["User"] != NULL:
            return 1
        else:
            return 0
    except:
        request.session["User"] = NULL
        return 2

def empty(request):
    if checklogin(request) == 1:
        return HttpResponseRedirect("/index/")
    else:
        return HttpResponseRedirect("/login/")

def index(request):
    if checklogin(request) == 1:
        return render(request, 'main/index.html',{
        "emp":login.objects.get(username = request.session["User"]).emp
         })
    else:
        return HttpResponseRedirect("/login/")  
    

def manage(request):                                                            
    if checklogin(request) != 1:
        return HttpResponseRedirect("/login/")
    projects = Projects.objects.filter(~Q(status = "C"))
    employees = Users.objects.filter(CurrentlyWorking = True)
    if login.objects.get(username = request.session["User"]).emp.role == "Manager":
        return render(request, 'main/manage.html',{
            "projects": projects,
            "employees": employees
        })
    else:
        return HttpResponseRedirect("/index/")

def login_site(request):
    if checklogin(request) == 1:
        request.session["User"] = NULL

    if request.method == 'POST':
        user = str(request.POST['username'])
        pwd = str(request.POST['password'])
        try:
            pwdverify = login.objects.get(username = user)
            print(pwdverify)
        except:
            return HttpResponse("<h2>User Does not Exist</h2>")
        if pwd == pwdverify.password:
            temp = login.objects.get(username = user)
            request.session["User"] = user
        else:
            return HttpResponse("<h2>Please Check your Password</h2>")
        return HttpResponseRedirect("/index/")
    try:
        if request.session["User"] == NULL:
            return render(request, 'main/login.html')
    except:
        request.session["User"] = NULL
        return render(request, 'main/login.html')
    return render(request, 'main/login.html')

def assigned_tasks(request):                                            #Views function for assigned tasks page
    if checklogin(request) != 1:
        return HttpResponseRedirect("/login/")
    
    user = login.objects.get(username = request.session["User"]).emp     
    tasks = assignments.objects.filter(asignee = user)
    #print(tasks)
    return render(request, "main/assigned.html",{
        "tasks" : tasks,
    })

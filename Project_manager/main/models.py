from datetime import date
from operator import mod
from pyexpat import model
from tkinter import CASCADE
from tkinter.tix import Balloon
from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    depts = (
        ("Electrical", "Electrical"),
        ("Mechanical", "Mechanical"),
        ("Software", "Software"),
        ("Admin", "Admin"),
        ("Other", "Other")
    )

    roles = (
        ("Manager", "Manager"),
        ("Team-Leader", "Team Leader"),
        ("Engineer", "Engineer"),
        ("Administrator", "Administrator"),
        ("Other", "Other")
    )
    user = models.ForeignKey(User, null = True, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    employeeID = models.IntegerField()
    designation = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    mail = models.EmailField(max_length=255)
    department=models.CharField(choices=depts, default="O", max_length=15)
    CurrentlyWorking = models.BooleanField(default=True)
    role = models.CharField(choices=roles, max_length=25,null=True )

    def __str__(self):
        return f"Name:{self.name}  (ID: {self.employeeID})"


class Projects(models.Model):
    st = (
        ("H", "On Hold"),
        ("P", "In Progress"),
        ("F", "Finished"),
        ("C", "Confirmed")
    )
    project_name = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=50)
    project_id = models.IntegerField()
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=True)
    status = models.CharField(choices=st, max_length=15)

    def __str__(self):
        return f"Project Name: {self.project_name}"


class tasks(models.Model):
    task = models.CharField(max_length=100)
    task_description = models.CharField(max_length=1000, blank=True)
    task_project = models.ForeignKey(Projects, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task} - {self.task_project}"


class assignments(models.Model):
    st = (
        ("On Hold", "H"),
        ("In Progress", "P"),
        ("Finished", "F"),
        ("Confirmed", "C"),
        ("Verified", "V")
    )
    asignee = models.ForeignKey(Users, on_delete=models.PROTECT)
    assigned_project = models.ForeignKey(Projects, on_delete=models.PROTECT)
    assigned_task = models.ForeignKey(tasks, on_delete=models.PROTECT)
    assignment_start_date = models.DateField(default=date.today)
    assignment_end_date = models.DateField(null= True)
    assignment_status = models.CharField(choices=st, max_length=15, default="C")
    time_req = models.FloatField(null = True)
    work_done = models.FloatField(default=0)
    work_done_temp = models.FloatField(default=0)
    def __str__(self):
        return f"{self.assigned_task.task} - {self.asignee.name}"


class login(models.Model):
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=30)
    emp = models.ForeignKey(Users, on_delete=models.CASCADE)



from django.contrib import admin
from django.forms import models

from .models import Users
from .models import Projects
from .models import assignments
from .models import tasks

admin.site.register(Users)
admin.site.register(assignments)
admin.site.register(Projects)
admin.site.register(tasks)
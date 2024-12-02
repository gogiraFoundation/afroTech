from django.shortcuts import render
from .models import Project

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'afro_engine/projects/project_list.html', {'projects': projects})

def homepage(request):
    return render(request, 'afro_engine/index.html')

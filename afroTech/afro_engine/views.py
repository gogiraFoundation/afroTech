from django.shortcuts import render
from django.views.generic import DetailView
from .models import Project, ProjectType


class ProjectTypeDetailView(DetailView):
    """
    'purpose': 'Handles the detail view for a single ProjectType.',
    'attributes': [
       'model': 'Specifies the ProjectType model.',
       'template_name': 'Path to the template used for rendering the detail view.'
       ]
    """
    model = ProjectType
    template_name = 'projecttypedetail.html'


class ProjectDetailView(DetailView):
    """
    'purpose': 'Handles the detail view for a single Project.',
    'attributes': [
       'model': 'Specifies the Project model.',
       'template_name': 'Path to the template used for rendering the detail view.'
    ]
    """
    model = Project
    template_name = 'project_detail.html'

def project_list(request):
    """
    'purpose': 'Displays a list of all projects along with their associated types.',
    'logic': [
        'Uses select_related to optimize database queries for related project_type.',
       'Passes the list of projects to the project_list.html template.'   
    ]
    """
    projects = Project.objects.select_related('project_type').all()
    return render(request, 'projects/project_list.html', {'projects': projects})



def homepage(request):
    """
    'purpose': 'Renders the homepage for the AfroTech application.',
    'logic': [
           'Directly renders the afro_engine/index.html template without additional context.'
    """
    return render(request, 'afro_engine/index.html')

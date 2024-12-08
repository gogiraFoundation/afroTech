from django.urls import path
from .views import ProjectTypeDetailView, ProjectDetailView, project_list, homepage


urlpatterns = [
    path('', homepage, name='home'),
    path('projects/', project_list, name='project_list'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projecttype/<int:pk>/', ProjectTypeDetailView.as_view(), name='projecttype-detail'),
]



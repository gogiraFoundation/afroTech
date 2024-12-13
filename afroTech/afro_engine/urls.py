from django.urls import path
from .views import (
    ProjectTypeDetailView, 
    ProjectDetailView, 
    ProjectListView,  # Use this if you want to list projects
    HomePageView,
    AboutUsView, 
    contact_view,
    newsletter_subscribe
)

app_name = 'afro_engine'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about-us/', AboutUsView.as_view(), name='about'),
    path('contact/', contact_view, name='contact'),
    path('projects/', ProjectListView.as_view(), name='project_list'),  # Corrected here
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projecttype/<int:pk>/', ProjectTypeDetailView.as_view(), name='projecttype-detail'),
    path('newsletter/subscribe', newsletter_subscribe, name='newsletter_subscribe'),
]

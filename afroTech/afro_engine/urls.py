
from django.urls import path
from afro_engine.views import project_list, homepage  # Corrected import

urlpatterns = [
    path('projects/', project_list, name='project_list'),
    path('home/', homepage, name="home"),  # Fixed missing slash
]
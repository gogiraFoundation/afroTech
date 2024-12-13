#views
from django.core.mail import BadHeaderError
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import DetailView, TemplateView, ListView
from .forms import ContactForm
from .models import Project, ProjectType, AboutUs, Newsletter
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
import logging

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
    context_object_name = 'project_type'


class ProjectDetailView(DetailView):
    """
    'purpose': 'Handles the detail view for a single Project.',
    'attributes': [
       'model': 'Specifies the Project model.',
       'template_name': 'Path to the template used for rendering the detail view.'
    ]
    """
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'


class ProjectListView(ListView):
    """
    'purpose': 'Displays a list of all projects along with their associated types.',
    'logic': [
        'Uses select_related to optimize database queries for related project_type.',
       'Passes the list of projects to the project_list.html template.'   
    ]
    """
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10

    def get_queryset(self):
        return Project.objects.select_related('project_type').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure pagination happens inside the context
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class HomePageView(TemplateView):
    """
    'purpose': 'Renders the homepage for the AfroTech application.',
    'logic': [
           'Directly renders the afro_engine/index.html template without additional context.'
    """
    template_name = 'afro_engine/index.html'

class AboutUsView(TemplateView):
    """
    'purpose':  renders the about-us page,
    'logic': [
            'Directly renders the afro_engine/about_us.html template without additional context'
    ]
    """
    template_name = 'afro_engine/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_us = AboutUs.objects.first()  # Assuming you have only one AboutUs entry
        if not about_us:
            context['error'] = "No About Us content available."
        else:
            context['about_us'] = about_us
        return context



def newsletter_subscribe(request):
    """
    Handles newsletter subscription.
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            if Newsletter.objects.filter(email__iexact=email).exists():
                messages.warning(request, "This email is already subscribed!")
            else:
                Newsletter.objects.create(email=email)
                messages.success(request, "Thank you for subscribing to our newsletter!")
        else:
            messages.error(request, "Please provide a valid email address.")
        return redirect('newsletter_subscribe')
    return render(request, 'newsletter/subscribe.html')



def contact_view(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        try:
            send_mail(
                subject=f"Message from {form.cleaned_data['name']}",
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['admin@afrotech.com'],
            )
            messages.success(request, 'Your message has been sent!')
            return redirect('contact')
        except BadHeaderError:
            messages.error(request, 'Invalid header found.')
            logger.error("Invalid header found while sending email.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            logger.error(f"Error sending email: {e}")
    return render(request, 'afro_engine/contact.html', {'form': form})
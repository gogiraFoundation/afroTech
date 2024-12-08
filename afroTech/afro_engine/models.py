from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db.models import Func

class Lower(Func):
    function = 'LOWER'

class ProjectType(models.Model):
    """
    'purpose': 'Defines categories or types for projects.',
    'fields': [
       'created_at': 'Timestamp for when the record was created.'
       ],
   'methods': [
       'get_absolute_url': 'Returns the URL to view details for a specific project type.',
       '__str__': 'String representation of the project type.'
       ],
    """
    STATUS_CHOICES = [
        ('DA', 'Data Analysis'),
        ('SW', 'Software Development'),
        ('DV', 'DevOps'),
        ('ML', 'Machine Learning'),
    ]
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='DA', help_text="Type of project (e.g., Data, Software).")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        'meta': [
            'verbose_name': 'Human-readable name for the model in singular form.',
            'verbose_name_plural': 'Human-readable name for the model in plural form.',
            'ordering': 'Default ordering by title in ascending order.',
            'constraints': 'Ensures title uniqueness in a case-insensitive manner.'
            ]
        """
        verbose_name = "Project Type"
        verbose_name_plural = "Project Types"
        ordering = ['status']

    def get_absolute_url(self):
        return reverse('projecttype-detail', args=[str(self.id)])

    def __str__(self):
        return self.get_status_display()

class Project(models.Model):
    title = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter the project title (e.g., Machine Learning Analysis)."
    )
    description = models.TextField(help_text="Enter a detailed project description.")
    project_type = models.ForeignKey(
        ProjectType, 
        on_delete=models.CASCADE, 
        related_name="projects", 
        help_text="Select the project type."
    )
    github_link = models.URLField(help_text="Link to the project's GitHub repository.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='projects/', 
        blank=True, 
        null=True, 
        help_text="Optional image for the project."
    )

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])

    def clean(self):
        if Project.objects.filter(
            title__iexact=self.title
        ).exclude(pk=self.pk).exists():
            raise ValidationError({
                'title': 'A project with this title already exists (case insensitive).'
            })

    def __str__(self):
        return f"{self.title} ({self.project_type.status})"

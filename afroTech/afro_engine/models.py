from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError


class ProjectType(models.Model):
    """
    'purpose': 'Defines categories or types for projects.',
    'fields': [
       'title': 'The name of the project type, unique and case-insensitive.',
       'github_link': 'Optional URL to a related GitHub repository.',
       'image': 'Optional image associated with the project type.',
       'created_at': 'Timestamp for when the record was created.'
       ],
   'methods': [
       'get_absolute_url': 'Returns the URL to view details for a specific project type.',
       '__str__': 'String representation of the project type.'
       ],
    
    """
    title = models.CharField(
        max_length=50,
        unique=True,
        help_text="Type of project (e.g., Data, Software)."
    )
    github_link = models.URLField(
        help_text="Link to the related GitHub repository."
    )
    image = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True,
        help_text="Optional image for the project type."
    )
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
        ordering = ['title']
        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='title_case_insensitive_unique',
            ),
        ]

    def get_absolute_url(self):
        return reverse('projecttype-detail', args=[str(self.id)])

    def __str__(self):
        return self.title



class Project(models.Model):
    """
    'purpose': 'Stores detailed information about individual projects.',
    'fields': [
       'title': 'The project title, unique and case-insensitive.',
       'description': 'A detailed description of the project.',
       'project_type': 'ForeignKey linking the project to a specific ProjectType.',
       'github_link': 'URL to the project’s GitHub repository.',
       'created_at': 'Timestamp for when the project was created.',
       'updated_at': 'Timestamp for when the project was last updated.'
   ],
   'methods': [
       'get_absolute_url': 'Returns the URL to view details for the specific project.',
       'save': 'Custom save method to enforce case-insensitive uniqueness for project types.',
       'clean': 'Validates case-insensitive uniqueness of the project title.',
       '__str__': 'String representation of the project with its type.'
   ],
    """
    title = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter the project title (e.g., Machine Learning Analysis)."
    )
    description = models.TextField(
        help_text="Enter a detailed project description."
    )
    project_type = models.ForeignKey(
        ProjectType,
        on_delete=models.RESTRICT,
        null=True,
        related_name="projects",
        help_text="Select the project type."
    )
    github_link = models.URLField(
        help_text="Link to the project's GitHub repository."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        'meta': [
            'verbose_name': 'Human-readable name for the model in singular form.',
            'verbose_name_plural': 'Human-readable name for the model in plural form.',
            'ordering': 'Default ordering by title in ascending order.'    
        """
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if ProjectType.objects.filter(
            title__iexact=self.project_type.title
        ).exclude(pk=self.pk).exists():
            raise ValueError("A ProjectType with this title already exists.")
        super().save(*args, **kwargs)

    def clean(self):
        if Project.objects.filter(
            title__iexact=self.title
        ).exclude(pk=self.pk).exists():
            raise ValidationError({
                'title': 'A project with this title already exists (case insensitive).'
            })

    def __str__(self):
        return f"{self.title} ({self.project_type.title})"

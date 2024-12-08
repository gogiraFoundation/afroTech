from django.db import models
from django.urls import reverse


class ProjectType(models.Model):
    title = models.CharField(max_length=50, unique=True, help_text="Type of project (e.g., Data, Software).")
    github_link = models.URLField(help_text="Link to the related GitHub repository.")
    image = models.ImageField(upload_to='projects/', blank=True, null=True, help_text="Optional image for the project type.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Project Type"
        verbose_name_plural = "Project Types"
        ordering = ['title']
        constraints = [
            UniqueConstraint(
                fields=['title'],
                name='title_case_insensitive_unique',
            ),
        ]

    def get_absolute_url(self):
        return reverse('projecttype-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=200, unique=True, help_text="Enter the project title (e.g., Machine Learning Analysis).")
    description = models.TextField(help_text="Enter a detailed project description.")
    project_type = models.ForeignKey(
        ProjectType,
        on_delete=models.RESTRICT,
        null=True,
        related_name="projects",
        help_text="Select the project type."
    )
    github_link = models.URLField(help_text="Link to the project's GitHub repository.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        if ProjectType.objects.filter(title__iexact=self.project_type.title).exclude(pk=self.pk).exists():
            raise ValueError("A ProjectType with this title already exists.")
        super().save(*args, **kwargs)
    
    def clean(self):
        if Project.objects.filter(title__iexact=self.title).exclude(pk=self.pk).exists():
            raise ValidationError({'title': 'A project with this title already exists (case insensitive).'})

    def __str__(self):
        return f"{self.title} ({self.project_type.title})"


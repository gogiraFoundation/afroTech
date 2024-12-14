from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db.models import Func
from django.core.validators import EmailValidator
from django.utils.text import slugify
from django.db import transaction
import logging

logger = logging.getLogger(__name__)


class Lower(Func):
    function = 'LOWER'


class ProjectType(models.Model):
    """
    Defines categories or types for projects.
    """
    STATUS_CHOICES = [
        ('DA', 'Data Analysis'),
        ('SW', 'Software Development'),
        ('DV', 'DevOps'),
        ('ML', 'Machine Learning'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DA',
        help_text="Type of project (e.g., Data Analysis, Software Development)."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Project Type"
        verbose_name_plural = "Project Types"
        ordering = ['status']

    def get_absolute_url(self):
        return reverse('projecttype-detail', args=[str(self.id)])

    def __str__(self):
        return self.get_status_display()

class Project(models.Model):
    """
    Represents an individual project with metadata and related information.
    """
    title = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter the project title (e.g., Machine Learning Analysis)."
    )
    slug = models.SlugField(
        unique=True,
        blank=True,  # Allow blank, because it will be auto-generated
        help_text="Unique slug for SEO-friendly URLs."
    )
    description = models.TextField(help_text="Enter a detailed project description.")
    project_type = models.ForeignKey(
        'ProjectType',  # Ensure 'ProjectType' is defined elsewhere
        on_delete=models.CASCADE,
        related_name="projects",
        help_text="Select the project type."
    )
    features = models.TextField(null=True, blank=True)
    technologies = models.CharField(max_length=255, null=True, blank=True)
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
        return reverse('project-detail', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        # Automatically generate a slug from the title if it's empty
        if not self.slug:
            self.slug = slugify(self.title)
        # Ensure slug is unique by appending a number if needed
        while Project.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{slugify(self.title)}-{Project.objects.filter(slug=self.slug).count() + 1}"

        super().save(*args, **kwargs)

    def clean(self):
        """
        Ensures the title and slug are unique, ignoring case sensitivity.
        """
        try:
            if self.slug is not None:
                if Project.objects.filter(title__iexact=self.title).exclude(pk=self.pk).exists():
                    raise ValidationError({
                        'title': 'A project with this title already exists (case insensitive).'
                    })
                if Project.objects.filter(slug__iexact=self.slug).exclude(pk=self.pk).exists():
                    raise ValidationError({
                        'slug': 'A project with this slug already exists (case insensitive).'
                    })
        except ValidationError as e:
            logger.warning(f"Validation error in Project: {e}")
            raise  # Re-raise the validation error
        except Exception as e:
            logger.error(f"Unexpected error cleaning Project: {e}")
            raise

    def __str__(self):
        return f"{self.title} ({self.project_type.status})"


class Contact(models.Model):
    """
    Represents a contact form submission.
    """
    name = models.CharField(max_length=100, help_text="Enter your full name.")
    email = models.EmailField(validators=[EmailValidator()])
    message = models.TextField(help_text="Enter your message.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Form Submission"
        verbose_name_plural = "Contact Form Submissions"
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class Newsletter(models.Model):
    """
    Represents newsletter subscriptions.
    """
    email = models.EmailField(unique=True, help_text="Subscriber's email address.")
    subscribed_at = models.DateTimeField(auto_now_add=True)#
    is_active = models.BooleanField(default=True, help_text="Flag to indicate if the subscription is active.")

    class Meta:
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
        ordering = ['-subscribed_at']

    def __str__(self):
        return f"Newsletter Subscription: {self.email}"


class AboutUs(models.Model):
    """
    Represents information for the About Us page.
    """
    content = models.TextField(help_text="Content for the About Us page.")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"

    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
                if not self.pk and AboutUs.objects.exists():
                    raise ValidationError("There can only be one AboutUs entry.")
                super().save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving AboutUs: {e}")
            raise

    def __str__(self):
        return "About Us Content"
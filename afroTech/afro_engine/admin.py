from django.contrib import admin
from django.utils.html import format_html, strip_tags
from .models import Project, ProjectType
from django import forms

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    list_display = ('title', 'github_link', 'get_short_description', 'project_type')
    search_fields = ['title', 'description']
    list_filter = ('project_type',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('title',)
    raw_id_fields = ('project_type',)

    def get_short_description(self, obj):
        """Shortened version of the description for display."""
        desc = strip_tags(obj.description)[:75] + ('...' if len(obj.description) > 75 else '')
        return format_html(desc)

    get_short_description.short_description = 'Description'

class ProjectInline(admin.TabularInline):
    """Provides an inline form for Project instances within related models."""
    model = Project
    extra = 1
    fields = ('title', 'github_link', 'description', 'project_type')
    readonly_fields = ('created_at',)

class ProjectTypeAdmin(admin.ModelAdmin):
    """Customize the admin interface for the ProjectType model."""
    list_display = ('status', 'created_at')
    search_fields = ['status']
    readonly_fields = ('created_at',)
    ordering = ('status',)
    inlines = [ProjectInline]

class ProjectInstanceAdmin(admin.ModelAdmin):
    """Customize the admin interface for the ProjectInstance model."""
    list_display = ('project', 'instance_name', 'status', 'created_at')
    list_filter = ('status',)

# Customizing the admin site
admin.site.site_header = "AfroTech Admin Panel"
admin.site.site_title = "AfroTech Administration"
admin.site.index_title = "Welcome to AfroTech Admin"

# Registering models with their respective admin classes
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectType, ProjectTypeAdmin)
# admin.site.register(ProjectInstanceAdmin)

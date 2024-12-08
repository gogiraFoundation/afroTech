from django.contrib import admin
from django.utils.html import format_html, strip_tags
from .models import Project, ProjectType, ProjectInstance

class ProjectAdmin(admin.ModelAdmin):
    """
    'purpose': 'Customize the admin interface for the Project model.',
    'functions': [
        'list_display': 'Displays selected fields in the admin list view.',
        'search_fields': 'Allows searching by title or description.',
        'list_filter': 'Adds a filter sidebar for project type.'
        'readonly_fields': 'Marks created_at and updated_at fields as non-editable.',
        'ordering': 'Orders the projects alphabetically by title.',
        'raw_id_fields': 'Optimizes selection for the project_type field.',
        'get_short_description': 'Displays a truncated, sanitized version of the description.
    """
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
    """'purpose': 'Provides an inline form for Project instances within related models.',
    'functions': [
                'model': 'Specifies the Project model for inline editing.',
                'extra': 'Defines the number of empty forms displayed by default.'
                'fields': 'Determines the fields to display in the inline form.'
                'readonly_fields': 'Marks created_at as non-editable.'
        ]
    """
    model = Project
    extra = 1
    fields = ('title', 'github_link', 'description', 'project_type')
    readonly_fields = ('created_at',)



class ProjectTypeAdmin(admin.ModelAdmin):
    """
    'purpose': 'Customize the admin interface for the ProjectType model.',
    'functions': [
       'list_display': 'Displays title, github_link, and created_at in the list view.',
       'search_fields': 'Allows searching by title.',
       'readonly_fields': 'Marks created_at as non-editable.',
       'ordering': 'Orders the project types alphabetically by title.',
       'inlines': 'Includes an inline form for associated Project instances.'
       ]
    """
    list_display = ('title', 'github_link', 'created_at')
    search_fields = ['title']
    readonly_fields = ('created_at',)
    ordering = ('title',)
    inlines = [ProjectInline]


class ProjectInstanceAdmin(admin.ModelAdmin):
    """
    'purpose': 'Customize the admin interface for the ProjectInstance model.'
    'functions': [
        'list_display': 'Displays project, instance_name, status, and created_at.',
        'list_filter': 'Adds a filter sidebar for the status field.'
        ]
    """
    list_display = ('project', 'instance_name', 'status', 'created_at')
    list_filter = ('status',)


# Customizing the admin site
admin.site.site_header = "AfroTech Admin Panel"
admin.site.site_title = "AfroTech Administration"
admin.site.index_title = "Welcome to AfroTech Admin"

# Registering models with their respective admin classes
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectType, ProjectTypeAdmin)
admin.site.register(ProjectInstance, ProjectInstanceAdmin)

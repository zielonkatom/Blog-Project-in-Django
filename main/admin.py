from django.contrib import admin
from .models import Project, Tutorial, TutorialCategory, TutorialSeries
from tinymce.widgets import TinyMCE
from django.db import models
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }

admin.site.register(Tutorial, ProjectAdmin)
admin.site.register(TutorialCategory)
admin.site.register(TutorialSeries)
admin.site.register(Project, ProjectAdmin)

from django.db import models


class TutorialCategory(models.Model):
    """Create Tutorial Categories for Tutorials"""
    tutorial_category = models.CharField(max_length=200)
    category_summary = models.CharField(max_length=200)
    category_slug = models.SlugField(max_length=200, default="")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.tutorial_category


class TutorialSeries(models.Model):
    """Create Tutorial Series for Tutorial Categories"""
    tutorial_series = models.CharField(max_length=200)
    tutorial_category = models.ForeignKey(TutorialCategory,
                                          default=1,
                                          verbose_name="Category",
                                          on_delete=models.SET_DEFAULT)

    series_summary = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Series"

    def __str__(self):
        return self.tutorial_series


class Tutorial(models.Model):
    """Create tutorial model for Tutorials tab."""
    tutorial_title = models.CharField(max_length=200)
    tutorial_content_short = models.CharField(max_length=200)
    tutorial_content_long = models.TextField()
    tutorial_date = models.DateTimeField(auto_now_add=True)
    tutorial_slug = models.SlugField(max_length=200, default="")
    tutorial_series = models.ForeignKey(TutorialSeries,
                                        default=1,
                                        verbose_name="Series",
                                        on_delete=models.SET_DEFAULT)

    def __str__(self):
        return self.tutorial_title


# Create your models here.
class Project(models.Model):
    """Project created by me for the portfolio."""
    project_title = models.CharField(max_length=200)
    project_date = models.DateTimeField(auto_now_add=True)
    project_content_short = models.CharField(max_length=300,
                                             default="")
    project_content_long = models.TextField()
    project_slug = models.SlugField(max_length=200, default="")
    project_github = models.CharField(max_length=200,
                                      default="/")

    def __str__(self):
        return self.project_title

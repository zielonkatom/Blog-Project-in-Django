from django.shortcuts import render, redirect, HttpResponse
from .models import Project, Tutorial, TutorialSeries, TutorialCategory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import NewUserForm


# Create your views here.
def homepage(request):
    """Return homepage"""
    return render(request=request,
                  template_name='main/index.html')


def single_slug_tutorial(request, single_slug):
    categories = [c.category_slug for c in TutorialCategory.objects.all()]
    if single_slug in categories:
        matching_series = TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)
        series_urls = {}

        for m in matching_series.all():
            part_one = Tutorial.objects.filter(tutorial_series__tutorial_series = m.tutorial_series)
            series_urls[m] = part_one[0].tutorial_slug

        return render(request=request,
                      template_name='main/category.html',
                      context={"tutorial_series": matching_series, "part_ones": series_urls})

    tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]
    if single_slug in tutorials:
        this_tutorial = Tutorial.objects.get(tutorial_slug=single_slug)
        tutorials_from_series = Tutorial.objects.filter(tutorial_series__tutorial_series=this_tutorial.tutorial_series)
        this_tutorial_idx = list(tutorials_from_series).index(this_tutorial)
        return render(request=request,
                      template_name="main/tutorial_details.html",
                      context={'tutorial_details': this_tutorial,
                               'tutorials_from_series': tutorials_from_series,
                               'this_tutorial_idx': this_tutorial_idx})

    return HttpResponse(f"'{single_slug}' does not correspond to anything we know of!")


def single_slug_project(request, single_slug):
    projects = [p.project_slug for p in Project.objects.all()]
    if single_slug in projects:
        return render(request=request,
                      template_name="main/project_details.html",
                      context={"project_details": Project.objects.get(project_slug=single_slug)})

    return HttpResponse(f"'{single_slug}' does not correspond to anything we know of!")


# Create your views here.
def projects(request):
    """Render all project objects"""
    return render(request=request,
                  template_name='main/projects.html',
                  context={"projects": Project.objects.all().order_by('-project_date')})


def tutorials(request):
    return render(request=request,
                  template_name="main/categories.html",
                  context={"categories": TutorialCategory.objects.all().order_by('tutorial_category')})


def register(request):
    """Register a new user"""
    if request.method == "POST":
        form = NewUserForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            username = user.username
            messages.success(request, f"New account created: { username }")
            # Login after successful registration
            login(request, user)
            # Go back to the homepage
            return redirect('main:homepage')
        else:
            messages.error(request, f"Something went wrong. Try one more time.")

    else:
        form = NewUserForm()

    return render(request=request,
                  template_name='main/register.html',
                  context={'form': form})


def login_view(request):
    """Login a user"""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user is not None:

                login(request, authenticated_user)
                messages.success(request, f"You are now loggged in as: { username }")
                return redirect("main:homepage")

            else:
                messages.error(request, f"Invalid login or password")

        else:
            messages.error(request, f"Invalid login or password")

    form = AuthenticationForm()
    return render(request,
                  "main/login.html",
                  {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, f"Logged the user out.")
    return redirect('main:homepage')


def profile(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return HttpResponse("Hello " + username)

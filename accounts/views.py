from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import JobSeekerProfile
from .forms import JobSeekerProfileForm, RecruiterProfileForm, AccountUpdateForm

from .models import JobSeekerProfile, RecruiterProfile
from .forms import JobSeekerProfileForm, RecruiterProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm
from .decorators import recruiter_required, jobseeker_required



@login_required
def home(request):
    return render(request, "accounts/home.html")


def registerView(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            role = form.cleaned_data.get("role")

            group, created = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            messages.success(request, "Account created successfully ✅")
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


def loginView(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name="recruiter").exists():
                return redirect("recruiter_dashboard")
            elif user.groups.filter(name="job_seeker").exists():
                return redirect("jobseeker_dashboard")
            else:
                return redirect("home")

        else:
            messages.error(request, "Invalid email or password ❌")

    return render(request, "accounts/login.html")


def logoutView(request):
    logout(request)
    return redirect("login")



@login_required
def my_profile(request):
    if is_jobseeker(request.user):
        profile, created = JobSeekerProfile.objects.get_or_create(user=request.user)
        return render(request, "accounts/jobseeker_profile.html", {"profile": profile})

    if is_recruiter(request.user):
        profile, created = RecruiterProfile.objects.get_or_create(user=request.user)
        return render(request, "accounts/recruiter_profile.html", {"profile": profile})

    messages.error(request, "No role assigned ❌")
    return redirect("home")



@login_required
def edit_profile(request):
    account_form = AccountUpdateForm(request.POST or None, instance=request.user)

    if request.user.groups.filter(name="job_seeker").exists():
        profile, _ = JobSeekerProfile.objects.get_or_create(user=request.user)
        profile_form = JobSeekerProfileForm(
            request.POST or None,
            request.FILES or None,
            instance=profile
        )

    elif request.user.groups.filter(name="recruiter").exists():
        profile, _ = RecruiterProfile.objects.get_or_create(user=request.user)
        profile_form = RecruiterProfileForm(request.POST or None, instance=profile)

    else:
        messages.error(request, "No role assigned ❌")
        return redirect("home")

    if request.method == "POST":
        if account_form.is_valid() and profile_form.is_valid():
            account_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully ✅")
            return redirect("my_profile")

    return render(request, "accounts/edit_profile.html", {
        "account_form": account_form,
        "profile_form": profile_form
    })

@login_required
def view_jobseeker_profile(request, user_id):
    # Only recruiter can view
    if not request.user.groups.filter(name="recruiter").exists():
        messages.error(request, "Not allowed ❌")
        return redirect("home")

    jobseeker_user = get_object_or_404(get_user_model(), id=user_id)
    profile = get_object_or_404(JobSeekerProfile, user=jobseeker_user)

    return render(request, "accounts/view_profile.html", {"profile": profile})


def is_jobseeker(user):
    return user.groups.filter(name="job_seeker").exists()

def is_recruiter(user):
    return user.groups.filter(name="recruiter").exists()

@login_required
@jobseeker_required
def jobseeker_dashboard(request):
    if not request.user.groups.filter(name="job_seeker").exists():
        messages.error(request, "Access denied")
        return redirect("home")
    return render(request, "accounts/jobseeker_dashboard.html")

from .decorators import recruiter_required, jobseeker_required

@login_required
@recruiter_required
def recruiter_dashboard(request):
    if not request.user.groups.filter(name="recruiter").exists():
        messages.error(request, "Access denied")
        return redirect("home")
    return render(request, "accounts/recruiter_dashboard.html")

from .profile_checks import profile_complete_required
from .decorators import jobseeker_required

@login_required
@jobseeker_required
@profile_complete_required
def test_apply(request):
    return render(request, "accounts/test_apply.html")


from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import JobSeekerProfile
from .decorators import recruiter_required
@login_required
@recruiter_required
def jobseeker_list(request):
    User = get_user_model()
    jobseekers = User.objects.filter(groups__name="job_seeker").distinct()
    return render(request, "accounts/jobseeker_list.html", {"jobseekers": jobseekers})

@login_required
@recruiter_required
def recruiter_view_jobseeker_profile(request, user_id):
    User = get_user_model()
    jobseeker_user = get_object_or_404(User, id=user_id, groups__name="job_seeker")

    profile, _ = JobSeekerProfile.objects.get_or_create(user=jobseeker_user)

    return render(request, "accounts/recruiter_view_jobseeker_profile.html", {
        "jobseeker_user": jobseeker_user,
        "profile": profile
    })

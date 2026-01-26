from django.shortcuts import redirect
from django.contrib import messages


def recruiter_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name="recruiter").exists():
            return view_func(request, *args, **kwargs)

        messages.error(request, "Recruiter access only ❌")
        return redirect("home")
    return wrapper


def jobseeker_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name="job_seeker").exists():
            return view_func(request, *args, **kwargs)

        messages.error(request, "Job seeker access only ❌")
        return redirect("home")
    return wrapper

from django.shortcuts import redirect
from django.contrib import messages
from .utils import is_jobseeker_profile_complete


def profile_complete_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not is_jobseeker_profile_complete(request.user):
            messages.error(request, "Complete your profile before applying ✅")
            return redirect("edit_profile")
        return view_func(request, *args, **kwargs)
    return wrapper

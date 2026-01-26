from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ("job_seeker", "Job Seeker"),
        ("recruiter", "Recruiter"),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ("email", "full_name", "role", "password1", "password2")

from django import forms
from django.contrib.auth import get_user_model
from .models import JobSeekerProfile, RecruiterProfile

User = get_user_model()


class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = [
            "contact_number",
            "graduation",
            "skills",
            "city",
            "resume",
            "github_url",
            "linkedin_url",
            "leetcode_url",
            "portfolio_url",
        ]



class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ["contact_number", "company_name", "designation", "company_website", "company_location"]


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name", "email"]

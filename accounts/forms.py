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

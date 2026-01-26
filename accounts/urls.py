from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.registerView, name="register"),
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutView, name="logout"),
    path("profile/", views.my_profile, name="my_profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/view/<int:user_id>/", views.view_jobseeker_profile, name="view_jobseeker_profile"),
    path("password-change/", auth_views.PasswordChangeView.as_view(template_name="accounts/password_change.html"), name="password_change"),
    path("password-change-done/", auth_views.PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"), name="password_change_done"),

    path("dashboard/jobseeker/", views.jobseeker_dashboard, name="jobseeker_dashboard"),
    path("dashboard/recruiter/", views.recruiter_dashboard, name="recruiter_dashboard"),
    path("test-apply/", views.test_apply, name="test_apply"),
    path("recruiter/jobseekers/", views.jobseeker_list, name="jobseeker_list"),
    path("recruiter/jobseekers/<int:user_id>/", views.recruiter_view_jobseeker_profile, name="recruiter_view_jobseeker_profile"),
    path("password-reset/", auth_views.PasswordResetView.as_view(
    template_name="accounts/password_reset.html"
), name="password_reset"),

path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
    template_name="accounts/password_reset_done.html"
), name="password_reset_done"),

path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
    template_name="accounts/password_reset_confirm.html"
), name="password_reset_confirm"),

path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
    template_name="accounts/password_reset_complete.html"
), name="password_reset_complete"),


]

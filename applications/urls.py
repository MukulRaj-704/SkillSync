from django.urls import path
from . import views

urlpatterns = [
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("jobs/<int:job_id>/applicants/", views.job_applicants, name="job_applicants"),
    path("my-applications/", views.my_applications, name="my_applications"),
    path("application/<int:app_id>/shortlist/", views.shortlist_application, name="shortlist_application"),
    path("application/<int:app_id>/reject/", views.reject_application, name="reject_application"),
    path("application/<int:app_id>/withdraw/", views.withdraw_application, name="withdraw_application"),


]

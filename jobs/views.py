from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.decorators import recruiter_required
from .models import Job
from .forms import JobForm


@login_required
@recruiter_required
def create_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, "Job posted successfully ✅")
            return redirect("job_list")
    else:
        form = JobForm()

    return render(request, "jobs/create_job.html", {"form": form})
from django.core.paginator import Paginator

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Job


def job_list(request):
    # base queryset (only open jobs)
    jobs = Job.objects.filter(is_active=True).order_by("-created_at")

    # filters
    title = request.GET.get("title", "")
    location = request.GET.get("location", "")
    company = request.GET.get("company", "")

    if title:
        jobs = jobs.filter(title__icontains=title)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if company:
        jobs = jobs.filter(company_name__icontains=company)

    # pagination
    paginator = Paginator(jobs, 5)  # 5 jobs per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "jobs/job_list.html", {
        "page_obj": page_obj,
        "title": title,
        "location": location,
        "company": company,
    })



from django.shortcuts import get_object_or_404

from django.shortcuts import get_object_or_404, render
from .models import Job

from applications.models import Application

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    is_job_seeker = False
    is_recruiter_owner = False
    has_applied = False
    application = None

    if request.user.is_authenticated:

        # JOB SEEKER LOGIC
        if request.user.groups.filter(name="job_seeker").exists():
            is_job_seeker = True

            application = Application.objects.filter(
                job=job,
                applicant=request.user
            ).first()

            # Applied / shortlisted / rejected = applied
            if application and application.status != "withdrawn":
                has_applied = True

        # RECRUITER OWNER LOGIC
        if request.user.groups.filter(name="recruiter").exists() and job.recruiter == request.user:
            is_recruiter_owner = True

    return render(request, "jobs/job_detail.html", {
        "job": job,
        "is_job_seeker": is_job_seeker,
        "is_recruiter_owner": is_recruiter_owner,
        "has_applied": has_applied,
        "application": application,
    })


@login_required
@recruiter_required
def close_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    job.is_active = False
    job.save()

    messages.success(request, "Job has been closed ❌")
    return redirect("recruiter_dashboard")






from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from jobs.models import Job
from .models import Application
from accounts.decorators import jobseeker_required
from accounts.profile_checks import profile_complete_required




@login_required
@jobseeker_required
@profile_complete_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # ❌ Job closed
    if not job.is_active:
        messages.error(request, "This job is no longer accepting applications ❌")
        return redirect("job_detail", job_id=job.id)

    application = Application.objects.filter(
        job=job,
        applicant=request.user
    ).first()

    # ❌ Block re-apply for active/rejected applications
    if application and application.status != "withdrawn":
        messages.warning(request, "You cannot re-apply for this job ⚠️")
        return redirect("job_detail", job_id=job.id)

    # ✅ Re-apply case (withdrawn → applied)
    if application and application.status == "withdrawn":
        application.status = "applied"
        application.save()
        messages.success(request, "Application re-submitted successfully ✅")
        return redirect("job_detail", job_id=job.id)

    # ✅ First-time apply
    Application.objects.create(
        job=job,
        applicant=request.user,
        status="applied"
    )

    messages.success(request, "Application submitted successfully ✅")
    return redirect("job_detail", job_id=job.id)



from accounts.decorators import recruiter_required
from django.shortcuts import render
from django.core.paginator import Paginator

@login_required
@recruiter_required
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)

    status_filter = request.GET.get("status")

    applications = Application.objects.filter(job=job)

    if status_filter == "shortlisted":
        applications = applications.filter(status="shortlisted")
    elif status_filter == "applied":
        applications = applications.filter(status="applied")

    applications = applications.exclude(status__in=["rejected", "withdrawn"]).select_related("applicant")
    
    paginator = Paginator(applications, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "applications/job_applicants.html", {
        "job": job,
        "applications": applications,
        "status_filter": status_filter,
    })


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import jobseeker_required
from .models import Application


@login_required
@jobseeker_required
def my_applications(request):
    applications = (
        Application.objects
        .filter(applicant=request.user)
        .select_related("job")
        .order_by("-applied_at")
    )

    return render(request, "applications/my_applications.html", {
        "applications": applications
    })


from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import recruiter_required
from .models import Application


@login_required
@recruiter_required
def shortlist_application(request, app_id):
    application = get_object_or_404(Application, id=app_id, job__recruiter=request.user)
    application.status = "shortlisted"
    application.save()

    messages.success(request, "Applicant shortlisted ✅")
    return redirect("job_applicants", job_id=application.job.id)


@login_required
@recruiter_required
def reject_application(request, app_id):
    application = get_object_or_404(Application, id=app_id, job__recruiter=request.user)
    application.status = "rejected"
    application.save()

    messages.warning(request, "Applicant rejected ❌")
    return redirect("job_applicants", job_id=application.job.id)


@login_required
@jobseeker_required
def withdraw_application(request, app_id):
    application = get_object_or_404(
        Application,
        id=app_id,
        applicant=request.user
    )

    if application.status != "applied":
        messages.error(request, "You cannot withdraw this application ❌")
        return redirect("my_applications")

    application.status = "withdrawn"
    application.save()

    messages.success(request, "Application withdrawn successfully")
    return redirect("my_applications")

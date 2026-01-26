from .models import JobSeekerProfile


def is_jobseeker_profile_complete(user):
    try:
        profile = JobSeekerProfile.objects.get(user=user)
    except JobSeekerProfile.DoesNotExist:
        return False

    # ✅ required text fields (must not be empty)
    def filled(value):
        return value is not None and str(value).strip() != ""

    basic_complete = (
        filled(profile.contact_number) and
        filled(profile.graduation) and
        filled(profile.skills) and
        filled(profile.city)
    )

    # ✅ resume OR at least one link required
    link_or_resume = bool(profile.resume) or any([
        filled(profile.github_url),
        filled(profile.linkedin_url),
        filled(profile.leetcode_url),
        filled(profile.portfolio_url),
    ])

    return basic_complete and link_or_resume

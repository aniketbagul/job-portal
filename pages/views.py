from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from jobs.choices import contract_choices, location_choices
from jobs.models import Job

# ✅ get custom user model (IMPORTANT FIX)
User = get_user_model()
from applications.models import Application


# 🌐 Home Page
def index(request):
    jobs = Job.objects.filter(is_published=True).order_by('-job_date')[:3]

    context = {
        'jobs': jobs,
        'location_choices': location_choices,
        'contract_choices': contract_choices
    }
    return render(request, 'pages/index.html', context)


# 📄 About Page
def about(request):
    return render(request, 'pages/about.html')


# 🔥 Custom Admin Dashboard
@login_required
def dashboard(request):
    if request.user.is_superuser:
        total_jobs = Job.objects.count()
        total_users = User.objects.count()
        total_applications = Application.objects.count()
    else:
        user_jobs = Job.objects.filter(creator=request.user)
        total_jobs = user_jobs.count()
        total_users = 0 # Not visible anyway
        user_job_ids = user_jobs.values_list('id', flat=True)
        total_applications = Application.objects.filter(job_id__in=user_job_ids).count()

    context = {
        'total_jobs': total_jobs,
        'total_users': total_users,
        'total_applications': total_applications,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def manage_users(request):
    if not request.user.is_superuser:
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, 'You do not have permission to view all users.')
        return redirect('dashboard')
    
    users = User.objects.all().order_by('-id')
    return render(request, 'dashboard/manage_users.html', {'users': users})
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Job
from .choices import location_choices, contract_choices


# 🌐 PUBLIC PAGES

def index(request):
    jobs = Job.objects.filter(is_published=True).order_by('-job_date')

    paginator = Paginator(jobs, 3)
    page_number = request.GET.get('page')
    paged_jobs = paginator.get_page(page_number)

    return render(request, 'jobs/jobs.html', {'jobs': paged_jobs})


def job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'jobs/job.html', {'job': job})


def search(request):
    jobs = Job.objects.filter(is_published=True).order_by('-job_date')

    if request.GET.get('role'):
        jobs = jobs.filter(role__icontains=request.GET['role'])

    if request.GET.get('location'):
        jobs = jobs.filter(location__iexact=request.GET['location'])

    if request.GET.get('contract'):
        jobs = jobs.filter(contract__iexact=request.GET['contract'])

    context = {
        'jobs': jobs,
        'location_choices': location_choices,
        'contract_choices': contract_choices,
        'values': request.GET
    }

    return render(request, 'jobs/search.html', context)


@login_required
def applyjob(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    if job.deadline < timezone.now():
        messages.error(request, 'Application deadline has passed!')
        return redirect('job', job_id=job.id)

    return render(request, 'jobs/applyjob.html', {'job': job})


# 🔥 CUSTOM ADMIN PANEL (YOUR OWN DASHBOARD)

@login_required
def manage_jobs(request):
    if request.user.is_superuser:
        jobs = Job.objects.all().order_by('-job_date')
    else:
        jobs = Job.objects.filter(creator=request.user).order_by('-job_date')
    return render(request, 'dashboard/manage_jobs.html', {'jobs': jobs})


@login_required
def add_job(request):
    if request.method == 'POST':
        main_image = request.FILES.get('main_image', '')
        Job.objects.create(
            creator=request.user,
            company=request.POST.get('company'),
            title=request.POST.get('title'),
            role=request.POST.get('role'),
            location=request.POST.get('location'),
            contract=request.POST.get('contract'),
            description=request.POST.get('description'),
            about=request.POST.get('about'),
            experience=request.POST.get('experience'),
            salary=request.POST.get('salary') or 0,
            vacancy=request.POST.get('vacancy'),
            deadline=request.POST.get('deadline'),
            main_image=main_image,
            is_published=True
        )

        messages.success(request, 'Job added successfully!')
        return redirect('manage_jobs')

    return render(request, 'dashboard/add_job.html')

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    # Check permission
    if not (request.user.is_superuser or request.user == job.creator):
        messages.error(request, 'You do not have permission to edit this job.')
        return redirect('manage_jobs')

    if request.method == 'POST':
        job.company = request.POST.get('company', job.company)
        job.title = request.POST.get('title', job.title)
        job.role = request.POST.get('role', job.role)
        if request.POST.get('location'):
            job.location = request.POST.get('location')
        if request.POST.get('contract'):
            job.contract = request.POST.get('contract')
        job.description = request.POST.get('description', job.description)
        job.about = request.POST.get('about', job.about)
        job.experience = request.POST.get('experience', job.experience)
        if request.POST.get('salary'):
            job.salary = request.POST.get('salary')
        job.vacancy = request.POST.get('vacancy', job.vacancy)
        if request.POST.get('deadline'):
            job.deadline = request.POST.get('deadline')
        if 'main_image' in request.FILES:
            job.main_image = request.FILES['main_image']
        
        job.save()
        messages.success(request, 'Job updated successfully!')
        return redirect('manage_jobs')

    # Format deadline for datetime-local input
    formatted_deadline = job.deadline.strftime('%Y-%m-%dT%H:%M') if job.deadline else ''

    return render(request, 'dashboard/edit_job.html', {'job': job, 'formatted_deadline': formatted_deadline})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    
    if not (request.user.is_superuser or request.user == job.creator):
        messages.error(request, 'You do not have permission to delete this job.')
        return redirect('manage_jobs')

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('manage_jobs')
    
    return redirect('manage_jobs')
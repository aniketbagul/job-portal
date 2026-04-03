from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from .models import Application
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from .analyzer import extract_text_from_file, analyze_resume_against_job

def application(request):
    if request.method == 'POST':
        job_id = request.POST['job_id']
        job = request.POST['job']
        creator = request.POST['creator']
        creator_id = request.POST['creator_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        resume = request.FILES['resume']
        user_id = request.POST['user_id']

        #  Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Application.objects.all().filter(job_id=job_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already applied for this job')
                return redirect('/jobs/'+job_id)    

        apply = Application(job=job, job_id=job_id,creator=creator,creator_id=creator_id, name=name, email=email, phone=phone,resume=resume, user_id=user_id)

        apply.save()


        messages.success(request, 'Your application has been submitted')
        return redirect('/jobs/'+ job_id)

@login_required
def manage_applications(request):
    if request.user.is_superuser:
        applications = Application.objects.all().order_by('-contact_date')
    else:
        # Get jobs created by this user
        user_job_ids = Job.objects.filter(creator=request.user).values_list('id', flat=True)
        applications = Application.objects.filter(job_id__in=user_job_ids).order_by('-contact_date')
        
    return render(request, 'dashboard/manage_applications.html', {'applications': applications})

@login_required
def analyze_resume(request, app_id):
    application = get_object_or_404(Application, pk=app_id)
    
    # Check permissions
    if not request.user.is_superuser:
        job = get_object_or_404(Job, pk=application.job_id)
        if job.creator != request.user:
            messages.error(request, "You do not have permission to view this application.")
            return redirect('manage_applications')
            
    # If there's no resume, we can't analyze
    if not application.resume:
        messages.error(request, "This applicant did not provide a parseable resume file.")
        return redirect('manage_applications')
        
    job = get_object_or_404(Job, pk=application.job_id)
    
    # 1. Get Resume Text
    # .path gives the absolute filesystem path to the uploaded file
    resume_text = extract_text_from_file(application.resume.path)
    
    if not resume_text:
        messages.error(request, "Could not extract text from the resume. It might be an image-only PDF or unsupported format.")
        return redirect('manage_applications')
        
    # 2. Analyze
    results = analyze_resume_against_job(resume_text, job.description, job.role)
    
    context = {
        'app': application,
        'job': job,
        'score': results['score'],
        'matched_keywords': results['matched'],
        'missing_keywords': results['missing'],
        'resume_preview': results['resume_preview']
    }
    
    return render(request, 'dashboard/resume_analysis.html', context)

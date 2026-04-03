from django.urls import path
from . import views
from jobs import views as job_views   # 🔥 import jobs views
from applications import views as application_views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),

    # Dashboard
    path('dashboard/', views.dashboard, name='admin_dashboard'),

    #from jobs import views as job_views

path('dashboard/jobs/', job_views.manage_jobs, name='manage_jobs'),
path('dashboard/jobs/add/', job_views.add_job, name='add_job'),
path('dashboard/jobs/edit/<int:job_id>/', job_views.edit_job, name='edit_job'),
path('dashboard/jobs/delete/<int:job_id>/', job_views.delete_job, name='delete_job'),
path('dashboard/applications/', application_views.manage_applications, name='manage_applications'),
path('dashboard/applications/analyze/<int:app_id>/', application_views.analyze_resume, name='analyze_resume'),
path('dashboard/users/', views.manage_users, name='manage_users'),
]
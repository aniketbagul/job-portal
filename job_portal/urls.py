from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views   # ✅ ADD THIS

urlpatterns = [
    path('staff/', admin.site.urls),

    # 🔐 Login / Logout
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Apps
    path('', include('pages.urls')),
    path('jobs/', include('jobs.urls')),
    path('accounts/', include('accounts.urls')),
    path('applications/', include('applications.urls')),
    path('contacts/', include('contacts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
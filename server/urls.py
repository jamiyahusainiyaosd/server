from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/academics', include('academics.urls')),
    path('api/v1/teacher', include('teacher.urls')),
    path('api/v1/contact', include('contact.urls')),
    path('api/v1/notices', include('notices.urls')),
    path('api/v1/admissions', include('admissions.urls')),
    path('api/v1/images', include('images.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
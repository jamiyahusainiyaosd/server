from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/academic/', include('academic.urls')),
    path('api/v1/teacher/', include('teacher.urls')),
    path('api/v1/contact/', include('contact.urls')),
    path('api/v1/notice/', include('notice.urls')),
    path('api/v1/admission/', include('admission.urls')),
    path('api/v1/image/', include('image.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
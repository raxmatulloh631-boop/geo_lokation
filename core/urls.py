from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views  # Login tizimi uchun

urlpatterns = [
    path('admin/', admin.site.urls),

    # Tayyor login oynasi URL'i (templates/login.html faylini ochib qo'ygan bo'lishingiz kerak)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # Ilovaning ichidagi barcha url'larni asosiy sahifaga ulaymiz
    path('', include('ilova.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
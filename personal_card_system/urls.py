from django.contrib import admin
from django.urls import path, include  # ← ЭТО ОБЯЗАТЕЛЬНО!
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cards.urls', namespace='cards')),
]

# ← Это обязательно для показа фото в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

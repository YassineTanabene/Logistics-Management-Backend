# mydrfproject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),  # Include the app's URLs



    path('reset-password', PasswordResetView.as_view(), name='password_reset'), 
    path('reset-password/done', PasswordResetDoneView.as_view(), name='password_reset_done'), 
    path('reset-password/confirm/<uidb64>[0-9A-Za-z]+)-<token>/', 
    PasswordResetConfirmView.as_view(), name='password_reset_confirm'), 
    path('reset-password/complete/',PasswordResetCompleteView.as_view(),
    name='password_reset_complete'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 

from .views import (
    login_request,
    logout_request,
    change_password,
)


urlpatterns = [
    path('join/login/', login_request, name="login"),
    path('join/logout/', logout_request, name="logout"),
    path('pages/change_password', change_password, name="change_password"),
]
urlpatterns += static(settings.MEDIA_URL,
                            document_root = settings.MEDIA_ROOT)
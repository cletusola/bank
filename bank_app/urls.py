from django.contrib import admin
from django.urls import path,include


from account.views import home 

urlpatterns = [
    path('', home, name="home"),
    path('admin/', admin.site.urls),
    path('account/', include("account.urls")),
    path('users/', include("users.urls")),
]

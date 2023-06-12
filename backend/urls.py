from authapp.views import login_page, signup_page
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from task.views import frontpage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontpage, name="frontpage"),
    path('login/', login_page, name="loginpage"),
    path('signup/', signup_page, name="signuppage"),
    path('auth/', include('authapp.urls')),
    path('api/', include('task.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib import admin
from django.urls import path, include
from django.http.response import HttpResponseRedirect

import mailinglist.urls
import user.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include(user.urls, namespace='user')),
    path('mailinglist/', include(mailinglist.urls, namespace='mailinglist')),
    path('', lambda x: HttpResponseRedirect('mailinglist'))
]

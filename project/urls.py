"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import url

#new
from .views import home, get_response
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    
     #path('', views.home, name='home'),
     #path('<str:room>/', views.room, name='room'),
     #path('checkview', views.checkview, name='checkview'),
     #path('send', views.send, name='send'),
     #path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    
    path('main/', include('main.urls')),
    path('',views.index, name='index'),
    path('admin/', admin.site.urls),
    path('candidate/',views.homeCandidate, name='candidate'),
    #path('adminProj/',views.homeAdmin, name='adminProj'),
    
    path('projectOwner/',views.homeProjectOwner, name='projectOwner'),
    path('moderator/',views.homeModerator, name='moderator'),
    #path('adminProj/adminProj/',views.homeAdmin, name='adminProj'),
    #new
    path('home/', home,name='home'),
    path('get-response/', get_response),
]

#new
if settings.DEBUG == True:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
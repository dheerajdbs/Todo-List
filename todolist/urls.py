"""todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home , name="home"),
    

    #Auth
    path('signup/', views.usersignup , name="usersignup"),
    path('logout/', views.userlogout , name="userlogout"),
    path('login/', views.userlogin , name="userlogin"),

    #ToDo
    path('current/', views.currenttodos , name="currenttodos"),
    path('create/', views.createtodos , name="createtodos"),
    path('current/<int:todo_id>/', views.tododesc , name="tododesc"),
    path('current/<int:todo_id>/complete/', views.completetodo , name="completetodo"),
    path('current/<int:todo_id>/delete/', views.deletetodo , name="deletetodo"),
    path('completed/', views.completedtodo , name="completedtodo"),
    
    
]

from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout , authenticate


def home(request):
    return render(request,"todo/home.html")

def usersignup(request):
    if request.method == "GET":
        return render(request,"todo/usersignup.html" , {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user =  User.objects.create_user(request.POST['username'] , password=request.POST['password1'])
                user.save()
            except IntegrityError:
                return render(request,"todo/usersignup.html" , {'form':UserCreationForm() , 'error':'Username Not Available.Please Choose a new Username'})
            else:
                login(request, user) 
                return redirect('currenttodos')

        else:
            return render(request,"todo/usersignup.html" , {'form':UserCreationForm() , 'error':'Passwords did not match'})


def userlogin(request):
    if request.method == "GET":
        return render(request,"todo/userlogin.html" , {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'] )
        if user is None:
            return render(request,"todo/userlogin.html" , {'form':AuthenticationForm() , 'error':"The Username and Password did not match"})
        else:
            login(request, user) 
            return redirect('currenttodos')

def currenttodos(request):
    return render(request,'todo/currenttodos.html')

def userlogout(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

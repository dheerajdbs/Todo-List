from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout , authenticate 
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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

@login_required
def createtodos(request):
    if request.method == "GET":
        return render(request,"todo/createtodos.html" , {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request,"todo/createtodos.html" , {'form':TodoForm() , 'error' : 'Bad Data Passed In.Please Try Again'})

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user = request.user , datecompleted__isnull = True)
    return render(request,'todo/currenttodos.html' , {'todos' : todos})

@login_required
def tododesc(request , todo_id):
    todo_id = get_object_or_404(Todo , pk = todo_id , user= request.user)
    if request.method == "GET":
        form = TodoForm(instance=todo_id)
        return render(request,"todo/tododesc.html" ,{'todo_id' : todo_id , 'form' : form})
    else:
        try:
            form = TodoForm(request.POST ,instance=todo_id)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request,"todo/tododesc.html" ,{'todo_id' : todo_id , 'form' : form , 'error' : "Bad Data Passed In.Please Try Again"})

@login_required
def userlogout(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

@login_required
def completetodo(request , todo_id):
    todo_id = get_object_or_404(Todo , pk = todo_id , user= request.user)
    if request.method == "POST":
        todo_id.datecompleted = timezone.now()
        todo_id.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request , todo_id):
    todo_id = get_object_or_404(Todo , pk = todo_id , user= request.user)
    if request.method == "POST":
        todo_id.delete()
        return redirect('currenttodos')

@login_required
def completedtodo(request):
    todos = Todo.objects.filter(user = request.user , datecompleted__isnull = False).order_by('-datecompleted')
    return render(request,'todo/completedtodo.html' , {'todos' : todos})


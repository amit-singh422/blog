from django.shortcuts import render,HttpResponseRedirect
from app.forms import SignupForm , LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from app.models import Post
from django.contrib.auth.models import Group



# Create your views here.

def home(request):
    posts=Post.objects.all()

    return render(request,'home.html',{'posts':posts})

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')


def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        ip=request.session.get('ip',0)
        return render(request,'dashboard.html',{'posts':posts,'ip':ip})
    else:
        return HttpResponseRedirect('/login/')

def user_logout(request):
    logout(request)
    return render(request,'logout.html')
    

def user_signup(request):
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            messages.success(request,'congratulations !! you became an author')
            user=form.save()
            group=Group.objects.get(name='author')
            user.groups.add(group)
    else:
        form=SignupForm()
    return render(request,'signup.html' , {'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form=LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'logged in successfully')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form=LoginForm()

        return render(request,'login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')
    


def add_post(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form=PostForm(request.POST)
            if form.is_valid():
                form.save()
                form=PostForm()
                return render(request,'addpost.html')
        else:
            form=PostForm()
            return render(request,'addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')
        



def update_post(request, id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=Post.objects.get(pk=id)
            form=PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                
        else:
            pi=Post.objects.get(pk=id)
            form=PostForm(instance=pi)
            return render(request,'addpost.html',{'form':form})

        return render(request,'updatepost.html')
    else:
        return HttpResponseRedirect('/login/')
    

def delete_post(request, id):
    if request.user.is_authenticated:
         if request.method=="POST":
            pi=Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
            

        
    else:
        return HttpResponseRedirect('/login/')
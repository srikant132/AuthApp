from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash                         #this is required to start login stuff
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm               # it include automatically form through  django
from django.contrib import messages                                                #It include some messaging features through django
from .forms import SignUpForm,EditProfileForm


# Create your views here.
def home(request):
    return render(request,'authenticateApp/home.html',{})

def login_user(request):
     if request.method == 'POST':                    #if the form method is post then we have apply condition
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(request, username=username, password=password)
          if user is not None:
              login(request, user)
              messages.success(request,('You have been logged In!'))
              return redirect('home')
          else:
              messages.success(request,('Error Logging In,Please Try Again...'))   #this show message
              return redirect('login')
     else:
         return render(request,'authenticateApp/login.html',{})


def logout_user(request):
    logout(request)
    messages.success(request,('You have been Logged Out...!'))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['Password1']
            password = form.cleaned_data['Password']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,('You have Registered...'))
            return redirect('home')
    else:
        form = SignUpForm(request.POST)
    context = {'form':form}
    return render(request,'authenticateApp/register.html',context)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST,instance=request.user)   #this will take data from database and appear to edit
        if form.is_valid():
            form.save()
            messages.success(request,('You have Edited Your Profile...'))
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)     #here the third argument instance passed for the reference user data
    context = {'form':form}
    return render (request,'authenticateApp/edit_profile.html',context)


def change_password(request):
    if request.method == 'POST':
        form =PasswordChangeForm (data=request.POST,user=request.user)   #to chanage password we use ChangePasswordForm that we imported
        if form.is_valid():                                              #also use third atrribute user=request.user and first attribute assign in data
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,('You have Edited Your Profile Password...'))
            return redirect('home')
    else:
        form =PasswordChangeForm(user=request.user)     # here also pass third attribute
    context = {'form':form}
    return render (request,'authenticateApp/change_password.html',context)

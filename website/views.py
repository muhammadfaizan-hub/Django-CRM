from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import  messages
from . forms import SignUpForm, AddRecordForm
from . models import Record



# Create your views here.
def home(request):
    records = Record.objects.all()
    # check if user is logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'Error logging in. Please try again....')
            return redirect('login')
    
    else:
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'Account was created for ' + username)
            return redirect('home')
        
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, 'You must loged in to access the page ')
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'Record deleted successfully')
        return redirect('home')
    else:
        messages.success(request, 'You must loged in to access the page ')
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Record added successfully')
                return redirect('home')
        else:
            return render(request, 'add_record.html',{'form':form})
    else:
        messages.success(request, 'You must loged in.....')
        return redirect('home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        update_it = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=update_it)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Record updated successfully')
                return redirect('home')
        else:
            return render(request, 'update_record.html',{'form':form})
    else:
        messages.success(request, 'You must loged in.....')
        return redirect('home')
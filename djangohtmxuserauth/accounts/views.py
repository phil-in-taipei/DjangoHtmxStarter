from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if request.htmx:
                return HttpResponse('<div class="success">Registration successful!</div>')
            return redirect('home')
        else:
            if request.htmx:
                return render(request, 'accounts/form_errors.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

@login_required
def home(request):
    return render(request, 'accounts/home.html')

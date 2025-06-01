from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.views import LoginView
from django.http import HttpResponse

from .forms import CustomUserCreationForm, UserProfileEditForm
from .models import UserProfile


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
    return render(request, 'home.html')


@login_required
def user_profile(request):
    """Display the user profile page or partial content"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        profile = UserProfile.objects.create(
            user=request.user,
            given_name='',
            surname=''
        )

    # Check if this is an htmx request for the form
    show_form = request.GET.get('show_form') == 'true'
    is_htmx = request.headers.get('HX-Request')

    context = {
        'user': request.user,
        'profile': profile,
    }

    if show_form:
        context['form'] = UserProfileEditForm(instance=profile)
        context['show_form'] = True

    # Return only the partial template for htmx requests
    if is_htmx:
        return render(request, 'accounts/profile_info_partial.html', context)

    # Return full page for regular requests
    return render(request, 'accounts/user_profile.html', context)

@login_required
@require_http_methods(["POST"])
def update_profile(request):
    """Handle htmx profile update request"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)

    form = UserProfileEditForm(request.POST, instance=profile)

    if form.is_valid():
        form.save()
        # Return the updated profile information as HTML
        context = {
            'user': request.user,
            'profile': profile,
            'edit_success': True
        }
        return render(request, 'accounts/profile_info_partial.html', context)
    else:
        # Return the form with errors
        context = {
            'user': request.user,
            'profile': profile,
            'form': form,
            'show_form': True
        }
        return render(request, 'accounts/profile_info_partial.html', context)
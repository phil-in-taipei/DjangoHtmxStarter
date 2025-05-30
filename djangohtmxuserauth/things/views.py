from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Thing


@login_required
def thing_list(request):
    print("getting thing list")

    """Display list of user's things"""
    user_profile = request.user.userprofile
    things = Thing.objects.filter(user_profile=user_profile)
    context = {
        'things': things,
        'user_profile': user_profile
    }
    print("getting thing list")
    return render(request, 'things/thing_list.html', context)


@login_required
@require_http_methods(["DELETE"])
def delete_thing(request, thing_id):
    """HTMX endpoint to delete a thing"""
    thing = get_object_or_404(Thing, id=thing_id, user_profile=request.user.userprofile)
    thing.delete()

    # Return empty response for HTMX to remove the table row
    return HttpResponse("")


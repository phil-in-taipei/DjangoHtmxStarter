from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from .forms import ThingForm
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


@login_required
@require_http_methods(["DELETE"])
def delete_thing(request, thing_id):
    """HTMX endpoint to delete a thing"""
    thing = get_object_or_404(Thing, id=thing_id, user_profile=request.user.userprofile)
    thing.delete()
    # Return empty response for HTMX to remove the table row
    return HttpResponse("")


@login_required
@require_http_methods(["POST"])
def create_thing(request):
    """HTMX endpoint to create a new thing"""
    form = ThingForm(request.POST)
    
    if form.is_valid():
        # Create the thing but don't save to DB yet
        thing = form.save(commit=False)
        # Set the user_profile
        thing.user_profile = request.user.userprofile
        # Now save to DB
        thing.save()
        
        # Return the new table row HTML
        description_display = thing.description if thing.description else '<em class="text-muted">No description</em>'
        if thing.description and len(thing.description) > 50:
            description_display = thing.description[:47] + '...'
            
        row_html = f"""
        <tr id="thing-{thing.id}" class="table-success">
            <td><strong>{thing.name}</strong></td>
            <td>{description_display}</td>
            <td><small class="text-muted">{thing.created_at.strftime('%b %d, %Y')}</small></td>
            <td>
                <button
                    class="btn btn-sm btn-outline-danger"
                    hx-delete="/things/delete/{thing.id}/"
                    hx-headers='{{"X-CSRFToken": "{request.META.get('CSRF_COOKIE', '')}""}}'
                    hx-target="#thing-{thing.id}"
                    hx-swap="outerHTML"
                    hx-confirm="Are you sure you want to delete '{thing.name}'?"
                    hx-on::after-request="if(event.detail.successful) {{ const count = document.getElementById('thing-count'); if(count) count.textContent = parseInt(count.textContent) - 1; }}"
                    title="Delete {thing.name}">
                    <i class="bi bi-trash"></i> Delete
                </button>
            </td>
        </tr>"""
        
        return HttpResponse(row_html)
    else:
        # Return form with errors - target the form container
        context = {'form': form}
        return render(request, 'things/partials/thing_form.html', context)

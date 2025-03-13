from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from functools import wraps

def manager_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_manager:
            return view_func(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('forbidden'))  # Or another restricted access page
    return _wrapped_view

def operator_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_operator:
            return view_func(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('forbidden'))
    return _wrapped_view

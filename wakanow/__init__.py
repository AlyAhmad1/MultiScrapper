from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def login_required(f):
    @wraps(f)
    def wrap(request):
        try:
            if request.session['user']:
                return f(request)
        except:
            messages.success(request, 'You Need To Login First')
            return redirect('login')
    return wrap

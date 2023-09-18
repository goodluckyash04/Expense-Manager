# decorators.py
from django.shortcuts import redirect
from .models import User

def auth_user(view_func):
    def wrapper(request, *args, **kwargs):
        if 'username' in request.session:
            username = request.session.get('username')
            user = None

            if username:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    pass

            # Add the 'user' parameter to the decorated view function's arguments only if it's used
            if 'user' in view_func.__code__.co_varnames:
                kwargs['user'] = user

            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper

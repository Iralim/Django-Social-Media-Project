from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

class UserTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                last_activity = request.session.get('last_activity')
                timeout_minutes = getattr(settings, 'USER_TIMEOUT_MINUTES', 30)
                
                if last_activity:
                    last_activity_time = datetime.fromisoformat(last_activity)
                    
                    if timezone.now() - last_activity_time > timedelta(minutes=timeout_minutes):
                        logout(request)
                        request.session.flush()
                        return redirect(f"{reverse('users:timeout')}?timeout=1")
                    
            except (ValueError, TypeError) as e:
                print(f"Encountered error {e} when trying to time out user {request.user.id}")
                logout(request)
                request.session.flush()

            finally:
                request.session['last_activity'] = timezone.now().isoformat()

        response = self.get_response(request)
        return response


from django.shortcuts import redirect

class RestrictAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        return response
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Define the paths you want to restrict
        restricted_paths = [
            '/account/login/',
            '/account/register/',
            '/account/password_reset/'
        ]
        
        # Check if user is authenticated and trying to access restricted pages
        if request.user.is_authenticated and request.path in restricted_paths:
            return redirect('blog:get_posts')  # Redirect to your home page
            
        return None  # Continue normal processing
from django.views.generic import ListView

from core.models import Post


class HomePage(ListView):
    """News listing"""

    model = Post
    template_name = 'home.html'

from django.contrib.auth.views import LoginView
from django.views.generic import ListView

from account.forms import SigninForm


# Create your views here.
class HomepageView(ListView):
    template_name = "account/home.html"
    context_object_name = "courses"


class SignInView(LoginView):
    template_name = "account/login.html"
    form_class = SigninForm
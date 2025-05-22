from django.contrib.auth.views import LoginView
from django.views.generic import ListView

from account import get_course_model
from account.forms import SigninForm

Course = get_course_model()

# Create your views here.
class HomepageView(ListView):
    template_name = "account/home.html"
    model = Course
    context_object_name = "courses"


class SignInView(LoginView):
    template_name = "account/login.html"
    form_class = SigninForm
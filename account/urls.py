from django.urls import re_path
from .views import HomepageView, SignInView

app_name = "account"

urlpatterns = [
    re_path(
        r"signin/$",
        SignInView.as_view(),
        name="signin"
    ),
    re_path(
        r"^$",
        HomepageView.as_view(),
        name="index"
    ),
]
from django.urls import re_path
from . import views

app_name = "course"

urlpatterns = [
    re_path(r"create/$", views.CourseCreateView.as_view(), name="course-create"),
    re_path(
        r"^trainers/create/$", views.TrainerCreateView.as_view(), name="trainer-create"
    ),
    re_path(
        r"^trainers/(?P<trainer_id>\d+)/change/$",
        views.TrainerUpdateView.as_view(),
        name="trainer-change",
    ),
    re_path(
        r"^(?P<course_id>\d+)/assign/$",
        views.AssignTrainerView.as_view(),
        name="course-assign",
    ),
]

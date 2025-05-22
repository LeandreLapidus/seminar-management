from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_course_model():
    """
    Return the User model that is active in this project.
    """
    try:
        return django_apps.get_model("course.Course", require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "'course.Course' has not been installed" % settings.AUTH_USER_MODEL
        )

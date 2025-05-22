import logging
from django.conf import settings
from django.db import transaction
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.template import loader
from django.views.generic import CreateView, UpdateView
from course.forms import CourseChangeForm, CourseCreateForm, TrainerForm
from course.models import Course, Trainer

# Create your views here.
logger = logging.getLogger("course")

class ObjectCreateMixin(CreateView):
    template_name = "course/edit.html"
    model = Course
    form_class = None
    success_url = reverse_lazy("account:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model"] = self.model.__name__
        return context
    


class CourseCreateView(ObjectCreateMixin):
    form_class = CourseCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create course")
        return context

class AssignTrainerView(UpdateView):
    template_name = "course/edit.html"
    form_class = CourseChangeForm
    pk_url_kwarg="course_id"
    model = Course
    success_url = reverse_lazy("account:index")
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Assign trainer")
        context["model"] = self.model.__name__
        return context
    
    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            trainer = self.object.trainer
            context = {
                "date": self.object.date_scheduled,
                "location": self.object.location,
                "name": self.object.name,
                "trainer": trainer.name,
            }
            self.send_mail(
                context,
                from_email=settings.EMAIL_HOST_USER,
                to_email=trainer.email)
            return HttpResponseRedirect(self.get_success_url())
    
    def send_mail(
        self,
        context,
        from_email,
        to_email,
        subject_template_name="email/notification_subject.txt",
        email_template_name="email/notification_content.html",
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context, self.request)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context, self.request)

        print(f"{context}\n\n")

        email_message = EmailMessage(subject, body, from_email, [to_email])
        email_message.send()
    

    

class TrainerCreateView(ObjectCreateMixin):
    form_class = TrainerForm
    model = Trainer
    success_url = reverse_lazy("account:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create trainer")
        return context
    
    

    
import logging
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages
from django.db import transaction
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
    pk_url_kwarg = "course_id"
    model = Course
    success_url = reverse_lazy("account:index")
    object: Course = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Assign trainer")
        context["suggestions"] = Trainer.objects.filter(
            subjects__icontains=self.object.subject
        ).exclude(courses__date_scheduled=self.object.date_scheduled)
        context["model"] = self.model.__name__
        return context

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            context = {
                "date": self.object.date_scheduled,
                "location": self.object.location,
                "name": self.object.name,
                "trainer": self.object.trainer.name,
                "notes": self.object.notes,
                "participants": self.object.participants,
                "trainer_price": self.object.trainer_price,
            }
            self.send_mail(
                context,
                from_email=settings.EMAIL_HOST_USER,
                to_email=self.object.trainer.email,
            )
            messages.info(
                self.request,
                message=_("A email has been sent to the trainer"),
                extra_tags="success",
            )
            return HttpResponseRedirect(self.get_success_url())

    def send_mail(
        self,
        context,
        from_email,
        to_email,
        subject_template_name="email/notification_subject.txt",
        email_template_name="email/notification_content.html",
    ):
        subject = loader.render_to_string(subject_template_name, context, self.request)

        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context, self.request)

        email_message = EmailMessage(subject, body, from_email, [to_email])
        email_message.send()


class TrainerCreateView(ObjectCreateMixin):
    form_class = TrainerForm
    model = Trainer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create trainer")
        return context


class TrainerUpdateView(UpdateView):
    form_class = TrainerForm
    model = Trainer
    template_name = "course/edit.html"
    pk_url_kwarg = "trainer_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Edit trainer")
        return context

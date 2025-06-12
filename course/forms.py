from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Field, Submit

from course.models import Course, Trainer


class CourseCreateForm(forms.ModelForm):

    class Meta:
        model = Course
        exclude = ["trainer"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.add_input(
            Submit("submit", _("Add course"), css_class="btn btn-primary")
        )
        self.helper.layout = Layout(
            Row(Field("subject"), css_class="mb-3"),
            Row(Field("name"), css_class="mb-3"),
            Row(Field("location"), css_class="mb-3"),
            Row(
                Field("date_scheduled", wrapper_class="col-lg-6"),
                Field("participants", wrapper_class="col-lg-6"),
                css_class="mb-3",
            ),
            Row(
                Field("price", wrapper_class="col-lg-6"),
                Field("trainer_price", wrapper_class="col-lg-6"),
                css_class="mb-3",
            ),
            Row(Field("notes"), css_class="mb-3"),
        )


class CourseChangeForm(forms.ModelForm):
    trainer = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label=_("Trainer"),
        help_text=_("Select a trainer for this course"),
    )

    class Meta:
        model = Course
        fields = ["subject", "name", "trainer"]

    def clean(self):
        trainer = self.cleaned_data.get("trainer", None)
        if trainer:
            date_scheduled = self.instance.date_scheduled
            is_trainer_scheduled = self.Meta.model.objects.filter(
                date_scheduled=date_scheduled, trainer=trainer
            ).exists()

            if is_trainer_scheduled:
                self.add_error(
                    "trainer",
                    forms.ValidationError(
                        _("This trainer is already scheduled for another course")
                    ),
                )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subject = self.instance.subject
        self.fields["trainer"].queryset = Trainer.objects.filter(
            subjects__icontains=subject
        )
        self.fields["subject"].disabled = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.add_input(
            Submit("submit", _("Assign trainer"), css_class="btn btn-primary")
        )
        self.helper.layout = Layout(
            Row(Field("subject"), css_class="mb-3"),
            Row(Field("name"), css_class="mb-3"),
            Row(Field("trainer"), css_class="mb-3"),
        )


class SubjectListField(forms.CharField):

    def to_python(self, value):
        """Return a list"""
        if value not in self.empty_values:
            value = str(value)
            if self.strip:
                value = value.strip()
        values = value.split(",")
        for i in range(len(values)):
            values[i] = values[i].strip()
        return values

    def prepare_value(self, value):
        if value:
            return ", ".join(value)
        return ""


class TrainerForm(forms.ModelForm):
    subjects = SubjectListField(
        max_length=255,
        required=True,
        help_text=_("Type each subjects separated with a comma"),
    )

    class Meta:
        model = Trainer
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.add_input(
            Submit("submit", _("Add trainer"), css_class="btn btn-primary")
        )
        self.helper.layout = Layout(
            Row(Field("subjects"), css_class="mb-3"),
            Row(Field("name"), css_class="mb-3"),
            Row(Field("email"), css_class="mb-3"),
            Row(Field("location"), css_class="mb-3"),
        )

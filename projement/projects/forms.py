from django.forms.models import ModelForm
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

from projects.models import Project


class ProjectForm(ModelForm):
    extra_design = forms.DecimalField(min_value=0, max_value=10000, decimal_places=2, required=False)
    extra_development = forms.DecimalField(min_value=0, max_value=10000, decimal_places=2, required=False)
    extra_testing = forms.DecimalField(min_value=0, max_value=10000, decimal_places=2, required=False)

    class Meta:
        model = Project
        fields = ['actual_design',  'extra_design', 'actual_development', 'extra_development', 'actual_testing', 'extra_testing']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'UPDATE'))
        self.helper.layout = Layout(
            Field('actual_design', readonly=True),
            'extra_design',
            Field('actual_development', readonly=True),
            'extra_development',
            Field('actual_testing', readonly=True),
            'extra_testing'
        )

    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()
        if cleaned_data["extra_design"]:
            cleaned_data['actual_design'] = cleaned_data["actual_design"] + cleaned_data["extra_design"]
        if cleaned_data["extra_development"]:
            cleaned_data['actual_development'] = cleaned_data["actual_development"] + cleaned_data["extra_development"]
        if cleaned_data["extra_testing"]:
            cleaned_data['actual_testing'] = cleaned_data["actual_testing"] + cleaned_data["extra_testing"]
        return cleaned_data

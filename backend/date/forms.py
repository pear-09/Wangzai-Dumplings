import json
from django import forms
import logging
logger = logging.getLogger(__name__)


class CreateDateForm(forms.Form):
    user_id = forms.IntegerField(required=False)
    title = forms.CharField(required=False)
    description = forms.CharField(required=False)
    time = forms.CharField(required=False)



class GenerateDatePlanForm(forms.Form):
    startday = forms.CharField()
    plan = forms.JSONField()
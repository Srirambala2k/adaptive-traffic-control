from django import forms
from .models import IncidentReport

class IncidentReportForm(forms.ModelForm):
    class Meta:
        model = IncidentReport
        fields = ["intersection", "description"]


class TrafficFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    intersection = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter intersection name'})
    )

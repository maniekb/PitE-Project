from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from bootstrap_datepicker_plus import DateTimePickerInput
from datetime import datetime
import pytz


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class RunArbitrageForm(forms.Form):
    amount = forms.DecimalField(label='Money amount', min_value=0.01, decimal_places=2)
    start_date = forms.DateTimeField(label='Search start time', widget=DateTimePickerInput())
    end_date = forms.DateTimeField(label='Search end time', widget=DateTimePickerInput())

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get("amount")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        time_diff = (end_date - start_date).total_seconds() / (3600*24)
        if start_date > end_date:
            msg = "End date must be later than start date"
            self.add_error('start_date', msg)
            self.add_error('end_date', msg)
            raise forms.ValidationError(msg)
        if end_date > pytz.utc.localize(datetime.now()):
            msg = "End date cannot be in the future"
            self.add_error('end_date', msg)
            raise forms.ValidationError(msg)
        if time_diff > 1.0:
            msg = "Time difference must be less than one day"
            self.add_error('start_date', msg)
            self.add_error('end_date', msg)
            raise forms.ValidationError(msg)
        if amount <= 0:
            msg = 'You must specify bigger amount of money'
            self.add_error('amount', msg)
            raise forms.ValidationError(msg)

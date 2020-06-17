from datetime import datetime, timedelta

import pytz
from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from kryptonite.userservice.user_service import get_all_currencies


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
    start_currency = forms.ChoiceField(choices=[(currency.value, currency.value) for currency in get_all_currencies()])
    amount = forms.DecimalField(label='Currency amount', min_value=0.01, decimal_places=2)
    start_date = forms.DateTimeField(label='Search start time', input_formats=["%d/%m/%Y %H:%M"],
                                     widget=DateTimePickerInput(format="%d/%m/%Y %H:%M"))
    end_date = forms.DateTimeField(label='Search end time', input_formats=["%d/%m/%Y %H:%M"],
                                   widget=DateTimePickerInput(format="%d/%m/%Y %H:%M"))
    include_margin = forms.BooleanField(label='Include margin', required=False)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        time_diff = (end_date - start_date).total_seconds() / (3600 * 24)
        if start_date > end_date:
            msg = "End date must be later than start date"
            self.add_error('start_date', msg)
            self.add_error('end_date', msg)
            raise forms.ValidationError(msg)
        if end_date - timedelta(hours=2) > pytz.utc.localize(datetime.utcnow()):
            msg = "End date cannot be in the future"
            self.add_error('end_date', msg)
            raise forms.ValidationError(msg)
        if time_diff > 1.0:
            msg = "Time difference must by at most one day"
            self.add_error('start_date', msg)
            self.add_error('end_date', msg)
            raise forms.ValidationError(msg)
        return self.cleaned_data

from django import forms

from core.form.base import TavaUpdateForm
from dashboard.models import Status
from ipam.models import Address
from django_select2 import forms as s2forms


class UpdateAddressForm(TavaUpdateForm):
    status = forms.ChoiceField(choices=((Status.AVAILABLE, 'Available'), (Status.USED, 'Used')),
                               widget=s2forms.Select2Widget, label="Current Status")

    def __init__(self, *args, **kwargs):
        super(UpdateAddressForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            raise forms.ValidationError("Please correct below errors")
        return cleaned_data

    class Meta:
        model = Address
        fields = ['status']
        widgets = {}

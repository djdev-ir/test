from django import forms

from core.form.base import TavaCreateForm
from dashboard.models import Status
from ipam.models import AddressRequest, AddressSubnet
from django_select2 import forms as s2forms


class CreateAddressRequestForm(TavaCreateForm):
    subnet = forms.ModelChoiceField(queryset=AddressSubnet.objects.all().exclude(status=Status.DELETED), widget=s2forms.Select2Widget,
                                    label="Subnet")

    def __init__(self, *args, **kwargs):
        super(CreateAddressRequestForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            raise forms.ValidationError("Please correct below errors")
        return cleaned_data

    class Meta:
        model = AddressRequest
        fields = ['subnet']
        widgets = {}

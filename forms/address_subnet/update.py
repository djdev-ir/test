from django import forms
from django.forms import ModelChoiceField
from django_select2 import forms as s2forms

from core.form.base import TavaUpdateForm
from ipam.models import AddressSubnet, AddressGroup


class UpdateAddressSubnetForm(TavaUpdateForm):
    parent = ModelChoiceField(queryset=AddressGroup.objects.all().exclude(is_trash=True), widget=s2forms.Select2Widget,
                              required=True, label="Group")

    def __init__(self, *args, **kwargs):
        super(UpdateAddressSubnetForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            raise forms.ValidationError("Please correct below errors")
        return cleaned_data

    class Meta:
        model = AddressSubnet
        fields = ['net_id', 'cidr', 'parent']
        widgets = {}

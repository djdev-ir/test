from django import forms
from core.form.base import TavaUpdateForm
from ipam.models import AddressGroup
from django_select2 import forms as s2forms


class UpdateAddressGroupForm(TavaUpdateForm):
    parent = forms.ModelChoiceField(queryset=None, widget=s2forms.Select2Widget, required=False)

    def __init__(self, *args, **kwargs):
        super(UpdateAddressGroupForm, self).__init__(*args, **kwargs)
        queryset = AddressGroup.objects.exclude(id=self.instance.id).exclude(is_trash=True)
        exclude_id = []
        for qs in queryset:
            qq = qs
            while qs.parent:
                if qs == self.instance:
                    exclude_id.append(qq.id)
                qs = qs.parent
            if qs == self.instance:
                exclude_id.append(qq.id)

        self.fields["parent"].queryset = queryset.exclude(id__in=exclude_id)

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            raise forms.ValidationError("Please correct below errors")
        return cleaned_data

    class Meta:
        model = AddressGroup
        fields = ['title', 'parent']
        widgets = {}

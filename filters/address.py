import django_filters
from crispy_forms.layout import Layout, Row, Column, Submit

from core.filter import TavaFilterSet
from dashboard.models import Status
from ipam.models import Address, AddressSubnet


class AddressFilter(TavaFilterSet):
    ip = django_filters.Filter(field_name="ip", label="IP Address", lookup_expr="contains")
    status = django_filters.ChoiceFilter(choices=((Status.AVAILABLE, 'Available'), (Status.RESERVED, 'Reserved'),
                                                  (Status.USED, 'Used')), label="Status",
                                         lookup_expr="icontains")

    parent = django_filters.ModelChoiceFilter(queryset=AddressSubnet.objects.all().exclude(status=Status.DELETED), label='Subnet')

    class Meta:
        model = Address
        fields = ['ip', 'status', "parent"]

    def __init__(self, *args, **kwargs):
        super(AddressFilter, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('ip', css_class='form-group col'),
                Column('status', css_class='form-group col'),
                Column('parent', css_class='form-group col'),
                Column(Submit('submit', 'Filter', css_class='btn-primary', style='margin: 28px 0;'), css_class="")
            )
        )
        self.helper.form_method = 'POST'

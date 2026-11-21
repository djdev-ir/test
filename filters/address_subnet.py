import django_filters
from crispy_forms.layout import Layout, Row, Column, Submit

from core.filter import TavaFilterSet
from ipam.models import AddressSubnet, AddressGroup


class AddressSubnetFilter(TavaFilterSet):
    net_id = django_filters.Filter(field_name="net_id", label="Network ID", lookup_expr="contains")
    cidr = django_filters.Filter(field_name="cidr", label="CIDR", lookup_expr="exact")
    parent = django_filters.ModelChoiceFilter(queryset=AddressGroup.objects.all().exclude(is_trash=True), label='Group')

    class Meta:
        model = AddressSubnet
        fields = ['net_id', 'cidr', "parent"]

    def __init__(self, *args, **kwargs):
        super(AddressSubnetFilter, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('net_id', css_class='form-group col'),
                Column('cidr', css_class='form-group col'),
                Column('parent', css_class='form-group col'),
                Column(Submit('submit', 'Filter', css_class='btn-primary', style='margin: 28px 0;'), css_class="")
            )
        )
        self.helper.form_method = 'POST'

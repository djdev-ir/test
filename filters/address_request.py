import django_filters
from crispy_forms.layout import Layout, Row, Column, Submit
from django.contrib.auth import get_user_model
from django.db.models import Min, Q

from core.filter import TavaFilterSet
from dashboard.models import Status
from ipam.models import AddressRequest, AddressSubnet


class AddressSubnetChoiceFilter(django_filters.ModelChoiceFilter):
    def filter(self, qs, value):
        if value:
            return qs.filter(
                Q(subnet__net_id=value.net_id) & Q(subnet__cidr=value.cidr)
            )
        return qs


def get_subnet_query(request=None):
    return AddressSubnet.objects.filter(
        id__in=[
            item['min_id'] for item in AddressSubnet.objects.values('net_id',
                                                                    'cidr').annotate(min_id=Min('id')).order_by()
        ]
    ).order_by("net_id")


class AddressRequestFilter(TavaFilterSet):
    applicant = django_filters.ModelChoiceFilter(queryset=get_user_model().objects.all(), label="Applicant")
    status = django_filters.ChoiceFilter(choices=((Status.REJECTED, 'Rejected'), (Status.ACCEPTED, 'Accepted')),
                                         label="Status", lookup_expr="icontains")

    subnet = AddressSubnetChoiceFilter(queryset=get_subnet_query, label='Subnet')

    assigned_address__ip = django_filters.Filter(field_name="assigned_address__ip", label="Assigned Address",
                                                 lookup_expr="icontains")

    class Meta:
        model = AddressRequest
        fields = ['applicant', "subnet", "assigned_address__ip", 'status']

    def __init__(self, *args, **kwargs):
        super(AddressRequestFilter, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('applicant', css_class='form-group col'),
                Column('subnet', css_class='form-group col'),
                Column('status', css_class='form-group col-2'),
                Column('assigned_address__ip', css_class='form-group col-2'),
                Column(Submit('submit', 'Filter', css_class='btn-primary', style='margin: 28px 0;'), css_class="")
            )
        )
        self.helper.form_method = 'POST'

from core.table.bit_base import BitBaseAllTable
from core.table.custom_columns import StatusColumn
from ipam.models import AddressRequest


class AllAddressRequestsTable(BitBaseAllTable):
    status = StatusColumn()

    class Meta:
        model = AddressRequest
        fields = ['applicant', "subnet", 'assigned_address', 'status']

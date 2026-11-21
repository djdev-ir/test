from django_tables2 import tables

from dashboard.models import Status
from core.table.bit_base import BitBaseAllTable
from core.table.buttons import UpdateButton
from core.table.custom_columns import StatusColumn, CustomDateTimeColumn, OperationColumn, IpAddressColumn
from ipam.models import Address


class AllAddressesTable(BitBaseAllTable):
    parent = tables.columns.Column(verbose_name="Subnet")
    Operation = OperationColumn(buttons=[
        UpdateButton(url="update-address", appearance_condition=lambda record: record.status != str(Status.RESERVED))
    ])
    status = StatusColumn()
    last_seen = CustomDateTimeColumn()
    ip = IpAddressColumn()

    class Meta:
        model = Address
        fields = ['ip', "status", 'parent', 'last_seen']

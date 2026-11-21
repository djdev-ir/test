from core.table.bit_base import BitBaseAllTable
from core.table.custom_columns import OperationColumn
from core.table.buttons import UpdateButton, DeleteButton
from ipam.models import AddressGroup


class AllAddressGroupsTable(BitBaseAllTable):
    Operation = OperationColumn(buttons=[
        UpdateButton(),
        DeleteButton(),
    ])

    class Meta:
        model = AddressGroup
        fields = ['title', 'parent']

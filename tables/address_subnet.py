from django.utils.safestring import mark_safe
from django_tables2 import tables

from core.table.bit_base import BitBaseAllTable
from core.table.buttons import UpdateButton, DeleteButton
from core.table.custom_columns import OperationColumn
from ipam.models import AddressSubnet


class AllAddressSubnetsTable(BitBaseAllTable):
    parent = tables.columns.Column(verbose_name="Group")

    space_usage = tables.columns.TemplateColumn(verbose_name="Space Usage",
                                                template_name=" ",
                                                orderable=False)
    Operation = OperationColumn(buttons=[
        UpdateButton(),
        DeleteButton(),
    ])

    def render_space_usage(self, record):
        progress = round(((record.used_count + 2) / record.total_count) * 100, 2)
        if progress < 33:
            status = "success"
        elif progress > 67:
            status = "danger"
        else:
            status = "warning"
        bar = f"""
            <div class="progress" style="height:100%">
                <div class="progress-bar progress-bar-striped bg-{status}" role="progressbar" style="width: {progress}%" aria-valuenow="{progress}" aria-valuemin="0" aria-valuemax="100"><div id="myBar">{progress}%</div></div>
            </div>
        """
        return mark_safe(f"{bar}")

    class Meta:
        model = AddressSubnet
        fields = ['net_id', 'cidr', 'parent']

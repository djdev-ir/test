from auth.mixins import AdminSuperAdminMixin, IpamModuleLicenseMixin
from assistelligent.settings import NORMAL, AT_IRANCELL, AT_SEPAH
from core.view.mixins.button import AddNewButtonMixin
from core.view.bit import BitTableFilterView
from ipam.filters.address_group import AddressGroupFilter
from ipam.models import AddressGroup
from ipam.tables.address_group import AllAddressGroupsTable


class AddressGroupListView(IpamModuleLicenseMixin, AdminSuperAdminMixin, AddNewButtonMixin, BitTableFilterView):
    model = AddressGroup
    queryset = AddressGroup.objects.all().exclude(is_trash=True).order_by('-id')
    table_class = AllAddressGroupsTable
    filterset_class = AddressGroupFilter
    filter_width = NORMAL
    app_type = [AT_IRANCELL, AT_SEPAH]

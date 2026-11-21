from auth.mixins import AdminSuperAdminMixin, IpamModuleLicenseMixin
from assistelligent.settings import NORMAL, AT_SEPAH, AT_IRANCELL
from core.view.bit import BitTableFilterView
from ipam.filters.address import AddressFilter
from ipam.models import Address
from ipam.tables.address import AllAddressesTable


class AddressListView(IpamModuleLicenseMixin, AdminSuperAdminMixin, BitTableFilterView):
    model = Address
    table_class = AllAddressesTable
    filterset_class = AddressFilter
    filter_width = NORMAL
    app_type = [AT_IRANCELL, AT_SEPAH]

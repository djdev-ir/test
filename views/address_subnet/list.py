from auth.mixins import AdminSuperAdminMixin, IpamModuleLicenseMixin
from assistelligent.settings import NORMAL, AT_IRANCELL, AT_SEPAH
from core.view.mixins.button import AddNewButtonMixin
from core.view.bit import BitTableFilterView
from ipam.filters.address_subnet import AddressSubnetFilter
from ipam.models import AddressSubnet
from ipam.tables.address_subnet import AllAddressSubnetsTable


class AddressSubnetListView(IpamModuleLicenseMixin, AdminSuperAdminMixin, AddNewButtonMixin, BitTableFilterView):
    model = AddressSubnet
    table_class = AllAddressSubnetsTable
    filterset_class = AddressSubnetFilter
    filter_width = NORMAL
    app_type = [AT_IRANCELL, AT_SEPAH]

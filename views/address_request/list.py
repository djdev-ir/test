from auth.mixins import ReadonlyOperatorMixin, IpamModuleLicenseMixin
from assistelligent.settings import WIDE, AT_IRANCELL, AT_SEPAH
from core.view.mixins.button import AddNewButtonMixin
from core.view.bit import BitTableFilterView
from ipam.filters.address_request import AddressRequestFilter
from ipam.models import AddressRequest
from ipam.tables.address_request import AllAddressRequestsTable


class AddressRequestListView(IpamModuleLicenseMixin, ReadonlyOperatorMixin, AddNewButtonMixin, BitTableFilterView):
    model = AddressRequest
    table_class = AllAddressRequestsTable
    filterset_class = AddressRequestFilter
    create_button_name = "Request"
    filter_width = WIDE
    app_type = [AT_IRANCELL, AT_SEPAH]

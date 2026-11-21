from auth.mixins import AdminSuperAdminMixin, IpamModuleLicenseMixin
from assistelligent.settings import AT_IRANCELL, AT_SEPAH
from dashboard.models import Status
from core.view.bit import BitRecoverableDeleteView

from ipam.models import AddressSubnet, Address, AddressGroup


class DeleteAddressSubnetView(IpamModuleLicenseMixin, AdminSuperAdminMixin, BitRecoverableDeleteView):
    model = AddressSubnet
    activity_type = "IPAM"
    app_type = [AT_IRANCELL, AT_SEPAH]

    def get_activity_content(self, form):
        return f'"{self.object}" address subnet has been deleted'

    def form_valid(self, form):
        trash = AddressGroup.objects.get(title="Trash")
        self.object.parent = trash
        Address.objects.filter(parent=self.object).update(status=Status.DELETED)

        return super().form_valid(form)

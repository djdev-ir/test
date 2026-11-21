from auth.mixins import AdminSuperAdminMixin, IpamModuleLicenseMixin
from assistelligent.settings import AT_IRANCELL, AT_SEPAH
from core.view.bit import BitUpdateView
from ipam.forms.address_group.update import UpdateAddressGroupForm
from ipam.models import AddressGroup


class UpdateAddressGroupView(IpamModuleLicenseMixin, AdminSuperAdminMixin, BitUpdateView):
    model = AddressGroup
    form_class = UpdateAddressGroupForm
    activity_type = "IPAM"
    app_type = [AT_IRANCELL, AT_SEPAH]

    def get_activity_content(self, form):
        return f'"{form.instance}" address group has been updated'

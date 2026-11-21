from auth.mixins import AdminSuperAdminMixin, IpamModuleLicenseMixin
from assistelligent.settings import AT_IRANCELL, AT_SEPAH
from core.view.bit import BitCreateView
from ipam.forms.address_group.create import CreateAddressGroupForm
from ipam.models import AddressGroup


class CreateAddressGroupView(IpamModuleLicenseMixin, AdminSuperAdminMixin, BitCreateView):
    model = AddressGroup
    form_class = CreateAddressGroupForm
    activity_type = "IPAM"
    app_type = [AT_IRANCELL, AT_SEPAH]

    def get_activity_content(self, form):
        return f'"{form.instance}" address group has been created'

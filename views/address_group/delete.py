from django.contrib import messages

from auth.mixins import AdminSuperAdminMixin, IpamModuleLicenseMixin
from assistelligent.settings import AT_SEPAH, AT_IRANCELL
from dashboard.models import Status
from core.view.bit import BitDeleteView
from ipam.models import AddressGroup


class DeleteAddressGroupView(IpamModuleLicenseMixin, AdminSuperAdminMixin, BitDeleteView):
    model = AddressGroup
    activity_type = "IPAM"
    app_type = [AT_IRANCELL, AT_SEPAH]

    def get_activity_content(self, form):
        return f'"{self.object}" address group has been deleted'

    def form_valid(self, form):
        if self.object.group_children.count() or self.object.subnet_children.exclude(status=Status.DELETED).count():
            form.add_error(None, "You cannot delete a group with children")
            messages.error(self.request, "You cannot delete a group with children")
            return super(DeleteAddressGroupView, self).form_invalid(form)

        return super(DeleteAddressGroupView, self).form_valid(form)

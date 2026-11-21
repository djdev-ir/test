from auth.mixins import AdminSuperAdminMixin, IpamModuleLicenseMixin
from assistelligent.settings import AT_IRANCELL, AT_SEPAH
from dashboard.models import Status
from core.view.bit import BitUpdateView
from ipam.forms.address.update import UpdateAddressForm
from ipam.models import Address


class UpdateAddressView(IpamModuleLicenseMixin, AdminSuperAdminMixin, BitUpdateView):
    model = Address
    form_class = UpdateAddressForm
    status_before_update = None
    activity_type = "IPAM"
    app_type = [AT_IRANCELL, AT_SEPAH]

    def get_activity_content(self, form):
        return f'"{form.instance}" address status has been updated'

    def get_object(self, queryset=None):
        obj = super(UpdateAddressView, self).get_object(queryset)
        self.status_before_update = obj.status
        return obj

    def form_valid(self, form):
        if form.instance.status != self.status_before_update:
            if form.instance.status == str(Status.USED):
                form.instance.parent.used_count += 1
                form.instance.parent.save()
            elif form.instance.status == str(Status.AVAILABLE):
                form.instance.parent.used_count -= 1
                form.instance.parent.save()

        return super().form_valid(form)

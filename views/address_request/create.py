from auth.mixins import IpamModuleLicenseMixin, OperatorMixin
from assistelligent.settings import AT_IRANCELL, AT_SEPAH
from core.view.bit import BitCreateView
from dashboard.models import Status
from ipam.forms.address_request.create import CreateAddressRequestForm
from ipam.models import AddressRequest


class CreateAddressRequestView(IpamModuleLicenseMixin, OperatorMixin, BitCreateView):
    model = AddressRequest
    form_class = CreateAddressRequestForm
    activity_type = "IPAM"
    app_type = [AT_IRANCELL, AT_SEPAH]

    def get_activity_content(self, form):
        if form.instance.status == Status.ACCEPTED:
            return f'address request on "{form.instance.subnet}" has been {form.instance.status}({form.instance.assigned_address} has been assigned)'
        else:
            return f'address request on "{form.instance.subnet}" has been {form.instance.status}'

    def form_valid(self, form):
        available_addresses = form.instance.subnet.address_children.filter(status=Status.AVAILABLE)
        if available_addresses.count():
            form.instance.status = Status.ACCEPTED
            address = available_addresses.first()
            form.instance.assigned_address = address
            address.status = Status.USED
            form.instance.subnet.used_count += 1
            form.instance.subnet.save()
            address.save()
        else:
            form.instance.status = Status.REJECTED

        form.instance.applicant = self.request.user
        return super().form_valid(form)

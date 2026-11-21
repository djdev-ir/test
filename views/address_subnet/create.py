import ipaddress

import ipaddr
from django.db import transaction

from auth.mixins import AdminSuperAdminMixin, IpamModuleLicenseMixin
from assistelligent.settings import AT_IRANCELL, AT_SEPAH
from dashboard.models import Status
from core.view.bit import BitCreateView
from ipam.forms.address_subnet.create import CreateAddressSubnetForm
from ipam.models import AddressSubnet, Address


class CreateAddressSubnetView(IpamModuleLicenseMixin, AdminSuperAdminMixin, BitCreateView):
    model = AddressSubnet
    form_class = CreateAddressSubnetForm
    activity_type = "IPAM"
    app_type = [AT_IRANCELL, AT_SEPAH]

    def get_activity_content(self, form):
        return f'"{form.instance}" address subnet has been created'

    def form_valid(self, form):
        for address_subnet in AddressSubnet.objects.all().exclude(id=form.instance.id).exclude(status=Status.DELETED):
            if ipaddr.IPNetwork(str(form.instance)).overlaps(ipaddr.IPNetwork(str(address_subnet))):
                form.add_error(None, "This network overlaps with existing networks!")
                return super().form_invalid(form)
        try:
            ip_range = ipaddress.IPv4Network(str(form.instance), strict=True)
        except ValueError:
            form.add_error(None, "This network ID is not valid!(host ID needs to be zero)")
            return super().form_invalid(form)
        form.instance.total_count = ip_range.num_addresses
        addresses = []
        for ip in ip_range:
            if ip == ip_range.broadcast_address or ip == ip_range.network_address:
                addresses.append(Address(ip=str(ip), status=Status.RESERVED, parent=form.instance))
            else:
                addresses.append(Address(ip=str(ip), status=Status.AVAILABLE, parent=form.instance))
        with transaction.atomic():
            form.instance.save()
            Address.objects.bulk_create(addresses)

        return super().form_valid(form)

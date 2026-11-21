import ipaddress

import ipaddr
from django.db import transaction

from auth.mixins import AdminSuperAdminMixin, IpamModuleLicenseMixin
from assistelligent.settings import AT_IRANCELL, AT_SEPAH
from dashboard.models import Status
from core.view.bit import BitUpdateView
from ipam.forms.address_subnet.update import UpdateAddressSubnetForm
from ipam.models import AddressSubnet, Address, AddressGroup


class UpdateAddressSubnetView(IpamModuleLicenseMixin, AdminSuperAdminMixin, BitUpdateView):
    model = AddressSubnet
    form_class = UpdateAddressSubnetForm
    activity_type = "IPAM"
    app_type = [AT_IRANCELL, AT_SEPAH]

    def get_activity_content(self, form):
        return f'"{form.instance}" address subnet has been updated'

    def form_valid(self, form):
        for address_subnet in AddressSubnet.objects.all().exclude(id=form.instance.id).exclude(status=Status.DELETED):
            if ipaddr.IPNetwork(str(form.instance)).overlaps(ipaddr.IPNetwork(str(address_subnet))):
                form.add_error(None, "This network overlaps with existing networks!")
                return super().form_invalid(form)

        addresses = []
        try:
            ip_range = ipaddress.IPv4Network(str(form.instance), strict=True)
        except ValueError:
            form.add_error(None, "This network ID is not valid!(host ID needs to be zero)")
            return super().form_invalid(form)
        ip_addresses = list(Address.objects.filter(parent=form.instance).values('ip', 'status', 'last_seen'))
        dict_addresses = {}
        for address in ip_addresses:
            dict_addresses[address["ip"]] = {"status": address["status"], "last_seen": address["last_seen"]}

        for ip in ip_range:
            if ip == ip_range.broadcast_address or ip == ip_range.network_address:
                if dict_addresses.get(str(ip), None):
                    addresses.append(Address(ip=str(ip), status=Status.RESERVED, parent=None,
                                             last_seen=dict_addresses[str(ip)]["last_seen"]))
                else:
                    addresses.append(Address(ip=str(ip), parent=None, status=Status.RESERVED, last_seen=None))
            else:
                if dict_addresses.get(str(ip), None):
                    if dict_addresses[str(ip)]["status"] != str(Status.RESERVED):
                        addresses.append(Address(ip=str(ip), status=dict_addresses[str(ip)]["status"], parent=None,
                                                 last_seen=dict_addresses[str(ip)]["last_seen"]))
                    else:
                        addresses.append(Address(ip=str(ip), status=Status.AVAILABLE, parent=None,
                                                 last_seen=dict_addresses[str(ip)]["last_seen"]))

                else:
                    addresses.append(Address(ip=str(ip), parent=None, status=Status.AVAILABLE, last_seen=None))

        with transaction.atomic():
            address_subnet = AddressSubnet.objects.create(net_id=form.instance.net_id, cidr=form.instance.cidr,
                                                          parent=form.instance.parent,
                                                          status=Status.INIT, total_count=ip_range.num_addresses)
            for address in addresses:
                address.parent = address_subnet
            form.instance.address_children.update(status=Status.DELETED)
            trash = AddressGroup.objects.get(title="Trash")
            form.instance.status = Status.DELETED
            form.instance.parent = trash
            form.instance.net_id = form.initial["net_id"]
            form.instance.cidr = form.initial["cidr"]
            Address.objects.bulk_create(addresses)
            address_subnet.used_count = address_subnet.address_children.filter(status=Status.USED).count()
            address_subnet.save()

        return super().form_valid(form)

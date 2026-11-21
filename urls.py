from django.urls import path

from ipam.views.address.list import AddressListView
from ipam.views.address.update import UpdateAddressView
from ipam.views.address_group.create import CreateAddressGroupView
from ipam.views.address_group.delete import DeleteAddressGroupView
from ipam.views.address_group.list import AddressGroupListView
from ipam.views.address_group.update import UpdateAddressGroupView
from ipam.views.address_request.create import CreateAddressRequestView
from ipam.views.address_request.list import AddressRequestListView
from ipam.views.address_subnet.create import CreateAddressSubnetView
from ipam.views.address_subnet.delete import DeleteAddressSubnetView
from ipam.views.address_subnet.list import AddressSubnetListView
from ipam.views.address_subnet.update import UpdateAddressSubnetView

urlpatterns = [
    # Address Group
    path('address_groups/', AddressGroupListView.as_view(), name='address-groups'),
    path('address_groups/create/', CreateAddressGroupView.as_view(), name='new-address-group'),
    path('address_groups/<int:pk>/update/', UpdateAddressGroupView.as_view(), name='update-address-group'),
    path('address_groups/<int:pk>/delete', DeleteAddressGroupView.as_view(), name='delete-address-group'),

    # Address Subnet
    path('address_subnets/', AddressSubnetListView.as_view(), name='address-subnets'),
    path('address_subnets/create/', CreateAddressSubnetView.as_view(), name='new-address-subnet'),
    path('address_subnets/<int:pk>/update/', UpdateAddressSubnetView.as_view(), name='update-address-subnet'),
    path('address_subnets/<int:pk>/delete', DeleteAddressSubnetView.as_view(), name='delete-address-subnet'),

    # Address
    path('addresses/', AddressListView.as_view(), name='addresses'),
    path('addresses/<int:pk>/update/', UpdateAddressView.as_view(), name='update-address'),

    # Address Request
    path('address_requests/', AddressRequestListView.as_view(), name='address-requests'),
    path('address_requests/create/', CreateAddressRequestView.as_view(), name='new-address-request'),
]

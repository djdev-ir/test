from django.conf.global_settings import AUTH_USER_MODEL
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint, Q

from dashboard.models import TimeStampMixin, Status


class AddressGroup(TimeStampMixin):
    title = models.CharField(max_length=255, verbose_name="Title")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='group_children',
                               verbose_name="Parent")
    is_trash = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["parent", "title"],
                name="unique_title_per_parent",
                condition=Q(parent__isnull=False),
                violation_error_message="A sibling with this title already exists."
            ),
            UniqueConstraint(
                fields=["title"],
                name="unique_title_for_null_parent",
                condition=Q(parent__isnull=True),
                violation_error_message="A sibling with this title already exists."
            ),
        ]


class AddressSubnet(TimeStampMixin):
    net_id = models.GenericIPAddressField(protocol="IPv4", max_length=15, verbose_name="Network ID")
    cidr = models.PositiveSmallIntegerField(validators=[MinValueValidator(16), MaxValueValidator(30)])
    parent = models.ForeignKey(AddressGroup, on_delete=models.CASCADE, related_name="subnet_children",
                               verbose_name="Parent")
    status = models.CharField(max_length=24, null=False, default=str(Status.INIT), verbose_name="Status")
    used_count = models.IntegerField(null=False, default=0, verbose_name="Used Count")
    total_count = models.IntegerField(null=False, default=0, verbose_name="Total Count")

    def __str__(self):
        return self.net_id + "/" + str(self.cidr)


class Address(TimeStampMixin):
    ip = models.GenericIPAddressField(protocol="IPv4", max_length=15, verbose_name="IP")
    status = models.CharField(max_length=24, verbose_name="Status")
    parent = models.ForeignKey(AddressSubnet, on_delete=models.CASCADE, related_name="address_children",
                               verbose_name="Parent")
    last_seen = models.DateTimeField(null=True, verbose_name="Last Seen")

    def __str__(self):
        return self.ip


class AddressRequest(TimeStampMixin):
    status = models.CharField(max_length=24, verbose_name="Status")
    subnet = models.ForeignKey(AddressSubnet, on_delete=models.CASCADE, related_name="requests",
                               verbose_name="Subnet")
    applicant = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="address_requests",
                                  verbose_name="User")
    assigned_address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE, related_name="requests",
                                         verbose_name="Assigned Address")

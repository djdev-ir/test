import django_filters
from crispy_forms.layout import Layout, Row, Column, Submit

from core.filter import TavaFilterSet
from ipam.models import AddressGroup


class AddressGroupFilter(TavaFilterSet):
    title = django_filters.Filter(field_name="title", label="Title", lookup_expr="icontains")
    parent = django_filters.ModelChoiceFilter(queryset=AddressGroup.objects.all().exclude(is_trash=True), label='Parent')

    class Meta:
        model = AddressGroup
        fields = ['title', 'parent']

    def __init__(self, *args, **kwargs):
        super(AddressGroupFilter, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col'),
                Column('parent', css_class='form-group col'),
                Column(Submit('submit', 'Filter', css_class='btn-primary', style='margin: 28px 0;'), css_class="")
            )
        )
        self.helper.form_method = 'POST'

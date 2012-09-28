from django.forms.widgets import Select
from django.utils.translation import ugettext_lazy as _

from caminae.core.models import TopologyMixin
from caminae.mapentity.filters import PolygonFilter, PythonPolygonFilter, YearFilter, YearBetweenFilter
from caminae.mapentity.widgets import GeomWidget

from caminae.land.filters import EdgeFilter

from .models import Intervention, Project


class PolygonTopologyFilter(PolygonFilter):
    def filter(self, qs, value):
        if not value:
            return qs
        lookup = self.lookup_type
        inner_qs = TopologyMixin.objects.filter(**{'geom__%s' % lookup: value})
        return qs.filter(**{'%s__in' % self.name: inner_qs})


class InterventionFilter(EdgeFilter):
    bbox = PolygonTopologyFilter(name='topology', lookup_type='intersects', widget=GeomWidget)
    year = YearFilter(name='date', widget=Select, label=_(u"Year"))

    class Meta(EdgeFilter.Meta):
        model = Intervention
        fields = EdgeFilter.Meta.fields + [
            'status', 'type', 'stake', # user
        ]


class ProjectFilter(EdgeFilter):
    bbox = PythonPolygonFilter(name='geom', widget=GeomWidget)
    in_year = YearBetweenFilter(name=('begin_year', 'end_year'), widget=Select,
                    label=_(u"Year of activity"))

    class Meta(EdgeFilter.Meta):
        model = Project
        fields = EdgeFilter.Meta.fields



from rhombus.lib.utils import cerr, cout
from genaf_base.lib import query as base_query
from spatools.lib.analytics import query as spatool_query
from spatools.lib.analytics import selector as spatool_selector

base_query.set_query_class( filter_class = spatool_selector.Filter)

class Query(base_query.Query, spatool_query.Query):

    def __init__(self, specs, dbhandler, **kwargs):
        base_query.Query.__init__(self, specs, dbhandler, **kwargs)
        # use self.specs which now contains spec class instances
        spatool_query.Query.__init__(self, self.specs, dbhandler)
        self.specs['filter'].marker_ids = dbhandler.get_locus_ids_from_panel_ids(self.specs['filter'].panel_ids)

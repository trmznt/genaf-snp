from genaf_snp.views.tools import *
from rhombus.lib import fsoverlay as fsoverlay

from spatools.lib.analytics import ld

def do_ld(query, userinstance, ns, *args, **kwargs):

	dbh = get_dbhandler()
	analytical_sets = query.get_filtered_analytical_sets()

	for analytical_set in analytical_sets:

		ld_mat = ld.calculate_r2( analytical_set )

	return True


class LDAnalysis(SNPAnalyticViewer):

	title = 'LD Analysis'
	info = ''

	callback = do_ld

	def format_result(self, result):

		html = div()
		html.add( div(self.title) )

		return html, ''
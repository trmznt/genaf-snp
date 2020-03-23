
from genaf_snp.views.tools import *


def do_allele_analysis(query, userinstance, ns, *args, **kwargs):

	analytical_sets = query.get_filtered_analytical_sets()

	allele_freqs = []

	for analytical_set in analytical_sets:

			transposed_variant_df = analytical_set.variant_df.transpose()

			allele_freqs.append(

				( analytical_set,
					[ l.value_counts() for l in transposed_variant_df.item()] )
			)

	raise RuntimeError()

	return True

class AlleleAnalysis(SNPAnalyticViewer):


	title = 'Allele Frequency Summary'
	info = ''

	callback = do_allele_analysis

	def format_result(self, result):

		html = div()
		html.add( div(self.title) )

		return html, ''




from genaf_snp.views.tools import *

@roles(PUBLIC)
def index(request):



	html = div()

	analysis_list = dl()[

		dt( a('Sample Summary', href='/analysis/summary'), class_='col-sm-3' ),
		dd('''This analysis reports the basic summary of the selected samples, such as number of samples
			per groups, etc''',
			class_='col-sm-9'),

		dt( a('Allele Frequency', href=request.route_url('analysis-allele')), class_='col-sm-3' ),
		dd(class_='col-sm-9')[
			'''
			This analysis provides the allele frequency for each group of samples.
			''',
			a('Click here for example.', href='/')
		],

		dt(class_='col-sm-3')[ a('Haplotype Analysis', href=request.route_url('analysis-haplotype'))],
		dd(class_='col-sm-9')[
			'''This analysis can be used to observe haplotype diversity and frequencies.
			'''
		],

		dt(class_='col-sm-3')[ a('FST Analysis', href=request.route_url('analysis-fst'))],
		dd(class_='col-sm-9')[
			'''This analysis estimates FST between groups of samples.
			'''
		],

		dt(class_='col-sm-3')[ a('PI (diversity) Analysis', href=request.route_url('analysis-pi'))],
		dd(class_='col-sm-9')[
			''' This analysis calculates nucleotide diversity between groups of samples.
			'''
		],

		dt(class_='col-sm-3')[ a('LD Analysis', href=request.route_url('analysis-ld'))],
		dd(class_='col-sm-9')[
			''' This analysis generate heat map showing LD of each genotype within groups of samples.
			'''
		],

		dt(class_='col-sm-3')[ a('PCA/PCoA Analysis', href=request.route_url('analysis-pca'))],
		dd(class_='col-sm-9')[
			''' This analysis generate either PCoA (Principal Coordinate Analysis) or
				PCA (Principal Component Analysis) plots over 1st to 4th dimension.
			'''
		],

		dt(class_='col-sm-3')[ a('NJ Tree', href=request.route_url('analysis-nj'))],
		dd(class_='col-sm-9')[
			''' This analysis generate an NJ-Tree based on a distance matrix based on
				the genotypes of each sample.
			'''
		],

		dt(class_='col-sm-3')[ a('COI Analysis', href=request.route_url('analysis-coi'))],
		dd(class_='col-sm-9')[
			'''	This analysis uses COIL to estimate Complexity of Infection (COI), which a metric
				similar to Multiplicity of Infection (MoI).
			'''
		],

	]

	html.add(
		h3('Analysis'),
		analysis_list
	)

	return render_to_response("genaf_base:templates/generics/page.mako",
                { 'html': html,
                },
                request = request)

from genaf_snp.views.tools import *
from rhombus.lib import fsoverlay as fso

import pandas as pd
import matplotlib.pyplot as plt
from spatools.lib.analytics import dist
from spatools.lib.analytics import ca

from itertools import combinations

def do_pca(query, userinstance, ns, *args, **kwargs): #q, user, ns=None):

    dbh = get_dbhandler()
    #df = dbh.get_allele_dataframe(None, None, None)
    #initial_sample_sets = query.get_sample_sets()
    #analytical_sets = query.get_analytical_sets()
    analytical_sets = query.get_filtered_analytical_sets()
    #variant_df = pd.pivot_table( df, index = 'sample_id', columns = 'locus_id', values='call',
    #            aggfunc = lambda x: x )
    #haplotype_sets = query.get_filtered_haplotype_sets()

    dimension = 3
    dm = dist.get_distance_matrix(analytical_sets)
    pca_res = ca.pcoa( dm, dim = dimension )


    fso_dir = get_fso_temp_dir(userinstance.login)
    plotfile_urls = []

    for (ax, ay) in combinations(range( dimension ), 2):
        plotfile = fso_dir.abspath + '/' + 'pcoa-%d-%d' % (ax, ay)
        plot_png = ca.plot_pca(pca_res, dm, ax, ay, plotfile + '.png')
        plot_pdf = ca.plot_pca(pca_res, dm, ax, ay, plotfile + '.pdf')
        plotfile_urls.append( (fso.get_urlpath(plot_png), fso.get_urlpath(plot_pdf)) )

    pca_data = ca.format_data(pca_res, dm)
    data_file = fso_dir.abspath + '/' + 'pcoa-data.txt'
    with open(data_file, 'w') as outfile:
        for r in pca_data:
            outfile.write( '\t'.join( r ) )
            outfile.write( '\n' )

    ns.result = { 'plotfile_urls': plotfile_urls, 'data_file': fso.get_urlpath(data_file) }

    return True


class PCAAnalysis(SNPAnalyticViewer):

    title = 'PCA/PCoA Analysis'
    info = ''

    callback = do_pca


    def format_result(self, result):

        html = div()
        html.add( div(self.title) )

        for (png, pdf) in result['plotfile_urls']:
            html.add(
                image(src=png),
                br(),
                p(a('Click here to get the plot as a PDF file', href=pdf)),
                )

        html.add(
            br(),
            'Download data file here: ',
            a('data.txt', href=result['data_file']),
        )

        return html, ''

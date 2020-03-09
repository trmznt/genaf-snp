from genaf_snp.views.tools import *
from rhombus.lib import fsoverlay as fso

import pandas as pd
import matplotlib.pyplot as plt
from spatools.lib.analytics import dist
from spatools.lib.analytics import ca

def do_pca(query, userinstance, ns, *args, **kwargs): #q, user, ns=None):

    dbh = get_dbhandler()
    df = dbh.get_allele_dataframe(None, None, None)

    variant_df = pd.pivot_table( df, index = 'sample_id', columns = 'locus_id', values='call',
                aggfunc = lambda x: x )


    D = dist.simple_distance(variant_df)

    DM = dist.DistanceMatrix(None)
    DM.M = D[0]

    dimension = 2
    res = ca.pcoa( DM, dim = dimension )

    fso_dir = get_fso_temp_dir(userinstance.login)

    axis = [ (0, 39), (40, 59), (60, 71), (72, 85), (86, 125), (126, 131) ]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    pca_matrix = res[0]
    pca_var = res[1]

    for (i1, i2) in axis:
        ax.scatter( pca_matrix[i1:i2, 0], pca_matrix[i1:i2, 1] )
    
    plotfile = fso_dir.abspath + '/pcoa.png'
    fig.savefig(plotfile)
    ns.result= { 'plot_url': fso.get_urlpath(plotfile) }

    return True


class PCAAnalysis(SNPAnalyticViewer):

    title = 'PCA/PCoA Analysis'
    info = ''

    callback = do_pca


    def format_result(self, result):

        html = div()
        html.add( div(self.title) )
        html.add(
                image(src=result['plot_url']),
                )

        return html, ''

from genaf_snp.views.tools import *
from rhombus.lib import fsoverlay as fso
from spatools.lib.analytics import dist
from spatools.lib.analytics.nj import plot_nj

def do_nj(query, userinstance, ns, *args, **kwargs): #q, user, ns=None):

    dbh = get_dbhandler()
    analytical_sets = query.get_filtered_analytical_sets()

    dm = dist.get_distance_matrix(analytical_sets)

    dbh = query.dbh
    fso_dir = get_fso_temp_dir(userinstance.login)

    tip_label = query.specs['options'].get('tip_label', 'S')
    label_callback = {
        'S': lambda x: dbh.get_sample_by_id(x).code,
        'I': None,
        'C': lambda x: dbh.get_sample_by_id(x).location.country,
        '1': lambda x: dbh.get_sample_by_id(x).location.level1,
        '2': lambda x: dbh.get_sample_by_id(x).location.level2,
        '3': lambda x: dbh.get_sample_by_id(x).location.level3,
        '4': lambda x: dbh.get_sample_by_id(x).location.level4,
        '-': lambda x: '-',
    }

    tree_type = {
            'F': 'fan', 'R': 'radial', 'U': 'unrooted', 'P': 'phylogram'
        }[query.specs['options'].get('tree_type', 'F')]
    branch_coloring = True #query.options.get('branch_coloring', 'Y') == 'Y'

    njplot_png = plot_nj(dm, fso_dir.abspath, 'png',
            label_callback = label_callback[tip_label], tree_type=tree_type, branch_coloring=branch_coloring)
    njplot_pdf = plot_nj(dm, fso_dir.abspath, 'pdf',
            label_callback = label_callback[tip_label], tree_type=tree_type, branch_coloring=branch_coloring)

    ns.result = { 'png_plot': fso.get_urlpath(njplot_png),
                'pdf_plot': fso.get_urlpath(njplot_pdf) }

    return True


class NJAnalysis(SNPAnalyticViewer):

    title = 'Neigbor-Joining Tree Analysis'
    info = ''

    callback = do_nj

    def get_form(self, jscode="", params={}):

        qform, jscode = super().get_form( jscode="", params={} )
        qform.get('genaf-query.custom-options').add(

            input_select('genaf-query.tree_type', 'Tree type', offset=2, size=3,
                value='U',
                options = [
                        ('U', 'unrooted'),
                        ('R', 'radial'),
                        ('F', 'fan'),
                        ('P', 'phylogram'),
                ],
                multiple=False,
                ),

            input_select('genaf-query.tip_label', 'Tip label', offset=2, size=3,
                value='I',
                options = [
                        ('I', 'No tip label'),
                        ('S', 'Sample code'),
                        ('C', 'Country'),
                        ('1', 'Level 1 administration'),
                        ('2', 'Level 2 administration'),
                        ('3', 'Level 3 administration'),
                        ('4', 'Level 4 administration'),
                        ('-', 'Character -'),
                ],
                multiple=False,
                ),
        )

        return qform, jscode

    def parse_form(self, params):
        d = super().parse_form(params)
        d['tree_type'] = params.get('genaf-query.tree_type', 'U')
        d['tip_label'] = params.get('genaf-query.tip_label', 'I')
        return d

    def params2specs(self, params, groups_id=None):
        specs = super().params2specs(params, groups_id=None)
        specs['options']['tree_type'] = params['tree_type']
        specs['options']['tip_label'] = params['tip_label']
        return specs

    def format_result(self, result):

        html = div()
        html.add( div(self.title) )

        html.add(
            image(src=result['png_plot']),
            p(a('Click here to get the plot as a PDF file!', href=result['pdf_plot']))
        )

        return html, ''

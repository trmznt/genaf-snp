from genaf_base.views.analysis import *
from rhombus.lib.roles import *


class SNPAnalyticViewer(AnalyticViewer):

    title = 'SNP Analysis Viewer Template'

    info = ''

    callback = None


    def parse_form(self, params):

        d = super().parse_form(params)
        d['panel_ids'] = [int(x) for x in params.getall('genaf-query.panel_ids')]
        d['genotype_calling'] = params.get('genaf-query.genotype_calling', 'H')
        d['allele_threshold'] = float(params.get('genaf-query.allele_threshold', 0.9))
        d['snp_threshold'] = float(params.get('genaf-query.snp_threshold', 0.9))

        return d


    def get_form(self, jscode="", params={}):
        qform, jscode = super().get_form(jscode, params)

        panels = self.dbh.get_panels()

        qform.get('genaf-query.allele-params').add(

            input_select('genaf-query.panel_ids', 'Panel code(s)', offset=2, size=3,
                value=params.get('genaf-query.panels', None),
                options = [ (p.id, p.code) for p in panels ],
                multiple=True,
            ),

            input_select('genaf-query.genotype_calling',  'Genotype calling', offset=2, size=3,
                value='H',
                options = [
                                ('H', 'Heterozygote calls'),
                                ('MN', 'Majority calls (use N for equal intensity/read ratio)'),
                                ('MR', 'Majority calls (use ref allele for equal intensity/read ratio)'),
                ],
                multiple=False,
            ),

            input_text('genaf-query.allele_threshold', 'Intensity/read threshold',
                offset=2, size=3,
                value=5,
            ),

            input_text('genaf-query.snp_threshold', 'SNP quality threshold',
                offset=2, size=3,
                value=0.9,
            ),
        )

        return qform, jscode


    def params2specs(self, params, groups_id=None):

        specs = super().params2specs(params, groups_id)
        specs['filter'] = {
            'marker_qual_threshold': params.get('snp_threshold', 0.9),
            'sample_qual_threshold': 0.9,
            'abs_threshold': params.get('allele_threshold', 5),
            'panel_ids': params.get('panel_ids', None)
        }

        return specs
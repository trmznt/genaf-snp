from genaf_base.views.analysis import *
from rhombus.lib.roles import *


class SNPAnalyticViewer(AnalyticViewer):

    title = 'SNP Analysis Viewer Template'

    info = ''

    callback = None


    def parse_form(self, params):

        d = super().parse_form(params)


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

            input_select('genaf-query.calling',  'Genotype calling', offset=2, size=3,
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

            input_text('genaf-query.SNP_cutoff', 'SNP quality cutoff',
                offset=2, size=3,
                value=0.5,
            ),
        )

        return qform, jscode

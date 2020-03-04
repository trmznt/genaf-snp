from genaf_base.views.analysis import *
from rhombus.lib.roles import *


class SNPAnalyticViewer(AnalyticViewer):

    title = 'SNP Analysis Viewer Template'

    info = ''

    callback = None


    def parse_form(self, params):

        d = super().parse_form(params)

        # these needs to be in AnalysisViewer.parse_form()

        d['batch_ids'] = params.get('genaf-query.batch_ids')
        # XXX: we need to check batch_ids here

        return d


    def get_form(self, jscode="", params={}):
        qform, jscode = super().get_form(jscode, params)


        # this should be in AnalysisViewer.get_form()

        if self.request.user.has_roles( SYSADM, DATAADM, SYSVIEW, DATAVIEW ):
            batches = self.dbh.get_batches( groups = None )
        else:
            batches = self.dbh.get_batches( groups = self.request.user.groups )

        qform.get('genaf-query.sample-source').add(

            input_select('genaf-query.batch_ids', 'Batch code(s)', offset=2, size=3,
                value=params.get('genaf-query.batches', None),
                options = [ (b.id, b.code) for b in batches ],
                multiple=True,
            ),

            # 
        )

        qform.get('genaf-query.sample-processing').add(

            input_select('genaf-query.sample_filtering', 'Sample filtering',
                offset=2, size=3,
                value='N',
                options = [ ('N', 'No futher sample filtering'),
                            ('M', 'Monoclonal samples'),
                        ]
                ),
            input_select('genaf-query.spatial_differentiation', 'Spatial differentiation',
                offset=2, size=3,
                value=-1,
                options = [ (-1, 'No spatial differentiation'),
                            (0, 'Country level'),
                            (1, '1st Administration level'),
                            (2, '2nd Administration level'),
                            (3, '3rd Administration level'),
                            (4, '4th Administration level') ]
                ),
            input_select('genaf-query.temporal_differentiation', 'Temporal differentiation',
                offset=2, size=3,
                value=0,
                options = [ (0, 'No temporal differentiation'),
                            (1, 'Yearly'),
                            (2, 'Quaterly')]
                ),
        )

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
        )

        return qform, jscode

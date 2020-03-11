import logging

log = logging.getLogger(__name__)

from genaf_base.views import *


class PanelViewer(object):

    def __init__(self, request):
        self.request = request
        self.dbh = get_dbhandler()
        self.locus = None


    @m_roles( PUBLIC )
    def index(self):

        panels = self.dbh.get_panels()

        html = div()[ h2('Panels') ]

        table, code = generate_panel_table(panels, self.request)
        html.add( table )

        return render_to_response('genaf_base:templates/generics/page.mako',
            {   'content': str(html),
                'code': code,
            },  request = self.request)

    @m_roles( PUBLIC )
    def view(self):

    	pass

def generate_panel_table(panels, request):

    table_body = tbody()

    not_guest = not request.user.has_roles( GUEST )

    for panel in panels:
        table_body.add(
            tr(
                td(literal('<input type="checkbox" name="panel-ids" value="%d" />' % panel.id)
                    if not_guest else ''),
                td( a(panel.code) ),
                td( len(panel.loci) ),
            )
        )

    panel_table = table(class_='table table-condensed table-striped')[
        thead(
            tr(
                th('', style="width: 2em"),
                th('Code'),
                th('N SNPs')
            )
        )
    ]

    panel_table.add( table_body )
    html = div(panel_table)
    code = ''

    return html, code
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

        html, code = generate_panel_table(panels, self.request)

        return render_to_response('genaf_base:templates/generics/page.mako',
            {   'content': str(html),
                'code': code,
            },  request = self.request)

    @m_roles( PUBLIC )
    def view(self):

    	pass
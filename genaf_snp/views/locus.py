import logging

log = logging.getLogger(__name__)

from genaf_snp.views import *


class LocusViewer(object):

    def __init__(self, request):
        self.request = request
        self.dbh = get_dbhandler()
        self.locus = None


    @m_roles( PUBLIC )
    def index(self):

        loci = self.dbh.get_loci()

        html = div()[ h2('Loci') ]

        table, code = generate_locus_table(loci, self.request)
        html.add(table)

        return render_to_response('genaf_base:templates/generics/page.mako',
            {   'content': str(html),
                'code': code,
            },  request = self.request)

    @m_roles( PUBLIC )
    def view(self):
        pass

def generate_locus_table(loci, request):

    table_body = tbody()

    not_guest = not request.user.has_roles( GUEST )

    for locus in loci:
        table_body.add(
            tr(
                td(literal('<input type="checkbox" name="locus-ids" value="%d" />' % locus.id)
                    if not_guest else ''),
                td( a(locus.refseq) ),
                td( a(locus.position) ),
                td( a(locus.code) ),
                td( a(locus.ref) ),
                td( a(locus.alt) ),
            )
        )

    locus_table = table(class_='table table-condensed table-striped')[
        thead(
            tr(
                th('', style="width: 2em"),
                th('Refseq'),
                th('Position'),
                th('Code'),
                th('Ref'),
                th('Alt'),
            )
        )
    ]

    locus_table.add( table_body )

    html = div(locus_table)
    code = ''

    return html, code

from pyramid.config import Configurator
from sqlalchemy import engine_from_config

#from rhombus import init_app
from rhombus.lib.utils import cerr, cout
from rhombus import init_app as rhombus_init_app, add_route_view, add_route_view_class

# set configuration and dbhandler
from genaf_base import includeme as genaf_base_includeme, init_app
from genaf_snp.scripts import run

# initialize view
from genaf_snp.views import *


def includeme( config ):
    """ this configuration must be included as the last order
    """

    print('genaf_snp:', config)

    config.include( genaf_base_includeme )

    config.add_static_view('static', 'static', cache_max_age=3600)

    # override assets here
    #config.override_asset('rhombus:templates/base.mako', 'genaf_snp:templates/base.mako')
    #config.override_asset('rhombus:templates/plainbase.mako', 'genaf_snp:templates/plainbase.mako')

    # add extension
    from genaf_base.views.sample import SampleViewer
    from genaf_snp.views.sample import SNPSampleExtensionViewer
    SampleViewer.set_extension_viewer(SNPSampleExtensionViewer)

    # add route and view for home ('/'), /login and /logout
    #config.add_route('home', '/')
    #config.add_view('genaf_snp.views.home.index', route_name='home')

    #config.add_route('login', '/login')
    #config.add_view('genaf_snp.views.home.login', route_name='login')

    #config.add_route('logout', '/logout')
    #config.add_view('genaf_snp.views.home.logout', route_name='logout')

    # add additional routes and views here

    add_route_view_class( config, 'genaf_snp.views.locus.LocusViewer', 'genaf.locus',
        '/locus',
        '/locus/@@action',
        '/locus/{id}@@edit',
        '/locus/{id}@@save',
        ('locus/{id}', 'view')

    )

    add_route_view_class( config, 'genaf_snp.views.panel.PanelViewer', 'genaf.panel',
        '/panel',
        '/panel/@@action',
        '/panel/{id}@@edit',
        '/panel/{id}@@save',
        ('/panel/{id}', 'view')

    )

    # analysis part

    config.add_route('analysis-allele', '/tools/allele')
    config.add_view('genaf_snp.views.tools.allele.AlleleAnalysis', route_name='analysis-allele')

    config.add_route('analysis-haplotype', '/tools/haplotype')
    config.add_view('genaf_snp.views.tools.haplotype.Haplotype', route_name='analysis-haplotype')

    config.add_route('analysis-pi', '/tools/pi')
    config.add_view('genaf_snp.views.tools.pi.PiAnalysis', route_name='analysis-pi')

    config.add_route('analysis-fst', '/tools/fst')
    config.add_view('genaf_snp.views.tools.fst.FSTAnalysis', route_name='analysis-fst')

    config.add_route('analysis-pca', '/tools/pca')
    config.add_view('genaf_snp.views.tools.pca.PCAAnalysis', route_name='analysis-pca')

    config.add_route('analysis-nj', '/tools/nj')
    config.add_view('genaf_snp.views.tools.nj.NJAnalysis', route_name='analysis-nj')

    config.add_route('analysis-coi', '/tools/coi')
    config.add_view('genaf_snp.views.tools.coi.COIAnalysis', route_name='analysis-coi')

    config.add_route('analysis-ld', '/tools/ld')
    config.add_view('genaf_snp.views.tools.ld.LDAnalysis', route_name='analysis-ld')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    cerr('genaf-snp main() is running...')

    # attach rhombus to /mgr url, include custom configuration
    config = init_app(global_config, settings, prefix='/mgr'
                    , include = includeme, include_tags = [ 'genaf.includes' ])

    return config.make_wsgi_app()

from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from rhombus import init_app
from rhombus.lib.utils import cerr, cout

# set configuration and dbhandler
from genaf_base import includeme as genaf_base_includeme
from genaf_snp.scripts import run

# initialize view
from genaf_snp.views import *


def includeme( config ):
    """ this configuration must be included as the last order
    """

    config.include( genaf_base_includeme )

    config.add_static_view('static', 'static', cache_max_age=3600)

    # override assets here
    #config.override_asset('rhombus:templates/base.mako', 'genaf_snp:templates/base.mako')
    #config.override_asset('rhombus:templates/plainbase.mako', 'genaf_snp:templates/plainbase.mako')

    # add route and view for home ('/'), /login and /logout
    #config.add_route('home', '/')
    #config.add_view('genaf_snp.views.home.index', route_name='home')

    #config.add_route('login', '/login')
    #config.add_view('genaf_snp.views.home.login', route_name='login')

    #config.add_route('logout', '/logout')
    #config.add_view('genaf_snp.views.home.logout', route_name='logout')

    # add additional routes and views here


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    cerr('genaf-snp main() is running...')

    # attach rhombus to /mgr url, include custom configuration
    config = init_app(global_config, settings, prefix='/mgr'
                    , include = includeme, include_tags = [ 'genaf.includes' ])

    return config.make_wsgi_app()

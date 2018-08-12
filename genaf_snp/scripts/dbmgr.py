# genaf-snp dbmgr will call spatools dbmgr

import sys, transaction

from rhombus.lib.utils import cout, cerr, cexit, get_dbhandler
from rhombus.scripts import setup_settings, arg_parser

def init_argparser(p = None):

    from spatools.lib import dbmgr

    if p is None:
        p = arg_parser('genaf-snp dbgmr')

    return dbmgr.init_argparser(p)


def main( args ):

    settings = setup_settings( args )

    if not args.test and args.commit:
        with transaction.manager:
            do_dbmgr( args, settings )
            cerr('** COMMIT database **')

    else:
        cerr('** WARNING -- running without database COMMIT **')
        if not args.test:
            keys = input('Do you want to continue [y/n]: ')
            if keys.lower()[0] != 'y':
                sys.exit(1)
        do_dbmgr( args, settings )


def do_dbmgr(args, settings, dbh=None):

    from spatools.lib import dbmgr

    if dbh is None:
        dbh = get_dbhandler(settings)
    print(dbh)

    dbmgr.do_dbmgr(args, dbh, warning=False)


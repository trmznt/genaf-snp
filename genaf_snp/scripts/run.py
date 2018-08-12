
import sys, os
import argparse

from rhombus.scripts.run import main as rhombus_main, set_config
from rhombus.lib.utils import cout, cerr, cexit

from genaf_snp.models.handler import DBHandler

def greet():
    cerr('command line utility for genaf-snp')


def usage():
    cerr('genaf_snp-run - command line utility for genaf-snp')
    cerr('usage:')
    cerr('\t%s scriptname [options]' % sys.argv[0])
    sys.exit(0)


set_config( environ='GENAF_CONFIG',
            paths = ['spatools.scripts.', 'genaf_snp.scripts.'],
            greet = greet,
            usage = usage,
            dbhandler_class = DBHandler,
            includes = [ 'genaf.includes']
)

main = rhombus_main




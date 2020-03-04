from genaf_snp.views.tools import *

def do_haplotype_summary(*args, **kwargs): #q, user, ns=None):

    raise RuntineError()

    if not ns:
        ns = DummyNS()

class Haplotype(SNPAnalyticViewer):

    title = 'Haplotype Summary'
    info = ''

    callback = do_haplotype_summary


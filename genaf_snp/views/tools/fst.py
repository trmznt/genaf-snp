from genaf_snp.views.tools import *

def do_fst(*args, **kwargs): #q, user, ns=None):

    raise RuntineError()

    if not ns:
        ns = DummyNS()

class FSTAnalysis(SNPAnalyticViewer):

    title = 'FST Analysis'
    info = ''

    callback = do_fst


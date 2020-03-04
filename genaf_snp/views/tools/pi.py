from genaf_snp.views.tools import *

def do_pi(*args, **kwargs): #q, user, ns=None):

    raise RuntineError()

    if not ns:
        ns = DummyNS()

class PiAnalysis(SNPAnalyticViewer):

    title = 'PI (Diversity) Summary'
    info = ''

    callback = do_pi
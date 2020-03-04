from genaf_snp.views.tools import *

def do_coi(*args, **kwargs): #q, user, ns=None):

    raise RuntineError()

    if not ns:
        ns = DummyNS()

class COIAnalysis(SNPAnalyticViewer):

    title = 'CoI (Complexity of Infection) Analysis'
    info = ''

    callback = do_coi

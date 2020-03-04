from genaf_snp.views.tools import *

def do_pca(*args, **kwargs): #q, user, ns=None):

    raise RuntineError()

    if not ns:
        ns = DummyNS()

class PCAAnalysis(SNPAnalyticViewer):

    title = 'PCA/PCoA Analysis'
    info = ''

    callback = do_pca


from genaf_snp.views import *

class SNPSampleExtensionViewer(object):

    def __init__(self, request, sample):
        self.request = request
        self.sample = sample


    def extend(self, html):

        # we extend the html
        html.add( div('SNP list') )

        table_body = tbody()

        genotypes = sorted([ (g.locus.refseq, g.locus.position, g.A, g.C, g.G, g.T) for g in self.sample.genotypes ])
        for (r,p,a,c,g,t) in genotypes:
            table_body.add(
                tr( td(r), td(p), td(a), td(c), td(g), td(t),
                )
            )

        genotype_table = table(class_='table table-condensed table-striped')[
            thead(
                tr(
                    th('Refseq'), th('Pos'), th('A'), th('C'), th('G'), th('T'),
                )
            )
        ]

        genotype_table.add( table_body )

        html.add(genotype_table)
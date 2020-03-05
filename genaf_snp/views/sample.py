
from genaf_snp.views import *

class SNPSampleExtensionViewer(object):

    def __init__(self, request, sample):
        self.request = request
        self.sample = sample


    def extend(self, html):

        # we extend the html
        html.add( div('SNP list') )

        table_body = tbody()

        genotypes = sorted([ (g.locus.refseq, g.locus.position, g.call) for g in self.sample.genotypes ])
        for (r,p,c) in genotypes:
            table_body.add(
                tr( td(r), td(p), td(c),
                )
            )

        genotype_table = table(class_='table table-condensed table-striped')[
            thead(
                tr(
                    th('Refseq'), th('Pos'), th('Allele'),
                )
            )
        ]

        genotype_table.add( table_body )

        html.add(genotype_table)
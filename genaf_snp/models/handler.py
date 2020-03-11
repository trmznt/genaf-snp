
from rhombus.lib.utils import cerr, cout, get_dbhandler_class
from genaf_snp.models import dbschema
from genaf_snp.lib.query import Query
from spatools.models.handler_interface import base_sqlhandler

class DBHandler(get_dbhandler_class(), base_sqlhandler):

    # add additional class references
    Sample = dbschema.SNPSample
    Locus = dbschema.Locus
    Panel = dbschema.Panel
    Genotype = dbschema.Genotype
    Query = Query


    def initdb(self, create_table=True, init_data=True, rootpasswd=None):
        """ initialize database """
        super().initdb(create_table, init_data, rootpasswd)
        if init_data:
            from .setup import setup
            setup(self)
            cerr('[genaf-snp] Database has been initialized')


    # add additional methods here

    def get_loci(self, ids=None):
        """ return loci
        """
        return self.Locus.query(self.session()).order_by(self.Locus.refseq, self.Locus.position).all()

    def get_locus_by_code(self, code):
        return self.Locus.query(self.session()).filter(self.Locus.code == code).one()

    def get_locus_by_pos(self, ref, pos):
        """ return locus """
        cerr('[%s %d]' % (ref, pos))
        return self.Locus.query(self.session()).filter(self.Locus.refseq == ref, self.Locus.position == pos).one()


    def get_panels(self, ids=None):
        """ return all available panels """
        q = self.Panel.query(self.session()).order_by(self.Panel.code)
        if ids:
            q = q.filter(self.Panel.id.in_( ids ))
        return q.all()

    def get_locus_ids_from_panel_ids(self, panel_ids=None):
        """ return a set of marker ids from panel ids """
        panels = self.get_panels( panel_ids )
        locus_ids = set()
        for p in panels:
            locus_ids.update( [l.id for l in p.loci] )
        return locus_ids


from rhombus.lib.utils import cerr, cout, get_dbhandler_class
from genaf_snp.models import dbschema
from spatools.models.handler_interface import base_sqlhandler

class DBHandler(get_dbhandler_class(), base_sqlhandler):

    # add additional class references
    Sample = dbschema.SNPSample
    Locus = dbschema.Locus
    Panel = dbschema.Panel
    Genotype = dbschema.Genotype


    def initdb(self, create_table=True, init_data=True, rootpasswd=None):
        """ initialize database """
        super().initdb(create_table, init_data, rootpasswd)
        if init_data:
            from .setup import setup
            setup(self)
            cerr('[genaf-snp] Database has been initialized')


    # add additional methods here


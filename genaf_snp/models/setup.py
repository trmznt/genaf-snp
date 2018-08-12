
#from genaf_snp.models import *
from rhombus.lib.utils import cerr, cexit

def setup( dbh ):

    dbh.EK.bulk_update( ek_initlist, dbsession=dbh.session() )

    adm_group = dbh.Group.search('_DataAdm_', dbsession=dbh.session())

    # create default batch
    batch = dbh.Batch( code = 'default', group_id = adm_group.id, assay_provider_id = adm_group.id,
               species='X', lastuser_id=1, public=0)
    cerr("INFO - default batch created.")
    dbh.session().add(batch)



from spatools.lib.const import *

def get_attributes( class_ ):
    return list( getattr(class_, n) for n in dir(class_) if not n.startswith('_'))

ek_initlist = [
    (   '@SYSNAME', 'System names',
        [
            ( 'genaf_snp'.upper(), 'genaf_snp' ),
        ]
    	),
    (   '@PEAK-TYPE', 'Peak types',
        get_attributes(peaktype)
        ),
    (   '@CHANNEL-STATUS', 'Channel status',
        get_attributes(channelstatus)
        ),
    (   '@ASSAY-STATUS', 'Assay status',
        get_attributes(assaystatus)
        ),
    (   '@ALIGN-METHOD', 'Ladder alignment method',
        get_attributes(alignmethod)
        ),
    (   '@SCANNING-METHOD', 'Peak scanning method',
        get_attributes(scanningmethod)
        ),
    (   '@ALLELE-METHOD', 'Allele methods',
        get_attributes(allelemethod)
        ),
    (   '@BINNING-METHOD', 'Binning methods',
        get_attributes(binningmethod)
        ),
    (   '@DYE', 'Dye type',
        dyes
        ),
    (   '@SPECIES', 'Species',
        [   ( 'X', 'Undefined' ),
        ]),
    (   '@REGION', 'Region name',
        [   ( '', 'Undefined' ),
        ]),
    (   '@EXTFIELD', 'Extended fields',
        []),
]

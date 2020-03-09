# snp.py -- SNP schema
# this should in-sync with spatools snp.py

# both Sequenom and Amplicon library are (going to be) supported.

from sqlalchemy import func
from sqlalchemy.orm import relationship, backref, dynamic_loader, deferred, reconstructor

from rhombus.models.core import *
from rhombus.models.ek import EK
from rhombus.models.user import User, Group
from rhombus.models.mixin import *

from rhombus.lib.utils import cerr, cout, get_dbhandler_class

from spatools.lib.mixin import SampleMixIn, LocusMixIn, GenotypeMixIn, PanelMixIn
from genaf_base.models.dbschema import Batch, Note


class SNPSample(get_dbhandler_class().Sample, SampleMixIn):

    __mapper_args__ = { 'polymorphic_identity': 1 }

# Panel <-> Locus relationship
locus_panel_table = Table('locus_panels', metadata,
    Column('id', types.Integer, Sequence('locus_panel_sequence', optional=True),
        primary_key=True),
    Column('locus_id', types.Integer, ForeignKey('locuses.id'), nullable=False),
    Column('panel_id', types.Integer, ForeignKey('panels.id'), nullable=False),
    UniqueConstraint( 'locus_id', 'panel_id')
)

class Locus(BaseMixIn, Base, LocusMixIn):

    __tablename__ = 'locuses'

    code = Column(types.String(16), nullable=False, unique=True)
    refseq = Column(types.String(16), nullable=False, server_default='')
    position = Column(types.Integer, nullable=False, server_default='')

    # bases
    ref = Column(types.String(1), nullable=False, server_default='N')
    alt = Column(types.String(1), nullable=False, server_default='N')
    alt2 = Column(types.String(1), nullable=False, server_default='N')
    alt3 = Column(types.String(1), nullable=False, server_default='N')

    flags = Column(types.Integer, nullable=False, server_default='0')
    remark = deferred(Column(types.String(1024), nullable=False, server_default=''))

    __table_args__ = ( UniqueConstraint( 'refseq', 'position'), )

    @classmethod
    def search(cls, code, session):

        q = cls.query(session).filter( func.lower(cls.code) == func.lower(code) )
        if q.count() == 0: return None
        return q.one()


class Panel(BaseMixIn, Base, PanelMixIn):

    __tablename__ = 'panels'

    code = Column(types.String(32), nullable=False, server_default='')
    flags = Column(types.Integer, nullable=False, server_default='0')
    remark = Column(types.String(1024), nullable=False, server_default='')

    loci = relationship(Locus, secondary=locus_panel_table, order_by = [Locus.refseq, Locus.position])


class Genotype(BaseMixIn, Base, GenotypeMixIn):

    __tablename__ = 'genotypes'

    locus_id = Column(types.Integer, ForeignKey('locuses.id', ondelete='CASCADE'),
        nullable=False)
    locus = relationship(Locus, uselist=False)

    sample_id = Column(types.Integer, ForeignKey('samples.id', ondelete='CASCADE'),
        nullable=False)
    sample = relationship(SNPSample, uselist=False,
                backref=backref('genotypes', lazy='dynamic', passive_deletes=True))
    """ link to sample """

    # count for Amplicon, intensity * 1000 for sequenom
    A = Column(types.Integer, nullable=False, server_default='0')
    T = Column(types.Integer, nullable=False, server_default='0')
    C = Column(types.Integer, nullable=False, server_default='0')
    G = Column(types.Integer, nullable=False, server_default='0')

    value = Column(types.Integer, nullable=False, server_default='0.0')
    raw_qual = Column(types.Float, nullable=False, server_default='0.0')
    norm_qual = Column(types.Float, nullable=False, server_default='0.0')

    # base type
    call = Column(types.String(1), nullable=False, default='N')

    flags = Column(types.Integer, nullable=False, server_default='0')

    __table_args__ = ( UniqueConstraint( 'locus_id', 'sample_id'), )

from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
client = Table('client', pre_meta,
    Column('name', VARCHAR(length=40)),
    Column('description', VARCHAR(length=400)),
    Column('user_id', INTEGER),
    Column('client_id', VARCHAR(length=40), primary_key=True, nullable=False),
    Column('client_secret', VARCHAR(length=55), nullable=False),
    Column('is_confidential', BOOLEAN),
    Column('_redirect_uris', TEXT),
    Column('_default_scopes', TEXT),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['client'].columns['user_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['client'].columns['user_id'].create()

from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nickname', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
)

author = Table('author', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=120)),
)

author_book = Table('author_book', post_meta,
    Column('author_id', Integer),
    Column('book_id', Integer),
)

book = Table('book', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=120)),
    Column('author_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].drop()
    post_meta.tables['author'].create()
    post_meta.tables['author_book'].create()
    post_meta.tables['book'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].create()
    post_meta.tables['author'].drop()
    post_meta.tables['author_book'].drop()
    post_meta.tables['book'].drop()

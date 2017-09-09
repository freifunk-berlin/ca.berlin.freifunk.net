"""add cert_expiry column

Revision ID: 31a7742584
Revises: 5730af27a86
Create Date: 2017-09-07 22:50:57.260545

"""

# revision identifiers, used by Alembic.
revision = '31a7742584'
down_revision = '5730af27a86'

from alembic import op
import sqlalchemy as sa
from ca import app,db

def upgrade():
    # SQLite cant add unique column
    if "sqlite" == db.get_engine(app).name:
        conn=op.get_bind()
        conn.execute("ALTER TABLE request rename to request_old;")
        conn.execute("CREATE TABLE request ( id VARCHAR(80) NOT NULL, email VARCHAR(120), generation_date DATE, cert_sn INT UNIQUE, cert_expire_date Date , PRIMARY KEY (id));")
        conn.execute("INSERT INTO request SELECT id, email, generation_date, cert_sn, NULL from request_old;")
        conn.execute("DROP TABLE request_old;")
    else:
        op.add_column('request', sa.Column('cert_expire_date', sa.Date(), nullable=True, unique=False))


def downgrade():
    # SQLite dosn't support "drop Column"
    if "sqlite" == db.get_engine(app).name:
        conn=op.get_bind()
        conn.execute("ALTER TABLE request RENAME TO request_old;")
        conn.execute("CREATE TABLE request ( id VARCHAR(80) NOT NULL, email VARCHAR(120), generation_date DATE, cert_sn INT UNIQUE, PRIMARY KEY (id));")
        conn.execute("INSERT INTO request SELECT id, email, generation_date, cert_sn from request_old;")
        conn.execute("DROP TABLE request_old;")
    else:
        op.drop_column('request', 'cert_expire_date')


"""init

Revision ID: e5c836cebbd7
Revises: 
Create Date: 2020-04-08 09:01:13.151903

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "e5c836cebbd7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION "pgcrypto";')
    op.execute('CREATE EXTENSION "uuid-ossp";')
    op.execute('CREATE EXTENSION "btree_gist";')


def downgrade():
    op.execute('DROP EXTENSION "uuid-ossp";')
    op.execute('DROP EXTENSION "pgcrypto";')
    op.execute('DROP EXTENSION "btree_gist";')

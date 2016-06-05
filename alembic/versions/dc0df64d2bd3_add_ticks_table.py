# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2016 Eugene Frolov <eugene@frolov.net.ru>
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Add ticks table

Revision ID: dc0df64d2bd3
Revises: 05ba899219b1
Create Date: 2016-06-03 23:00:15.861997

"""

# revision identifiers, used by Alembic.
revision = 'dc0df64d2bd3'
down_revision = '05ba899219b1'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'ticks',
        sa.Column('uuid', sa.String(36), primary_key=True),
        sa.Column('_instrument_uuid', sa.String(36),
                  sa.ForeignKey('instruments.uuid'),
                  nullable=False,),
        sa.Column('timestamp', sa.REAL, nullable=False, index=True),
        sa.Column('ask', sa.Float, nullable=False, index=True),
        sa.Column('bid', sa.Float, nullable=False, index=True),
        sa.Column('ask_volume', sa.Float),
        sa.Column('bid_volume', sa.Float)
    )


def downgrade():
    op.drop_table('ticks')

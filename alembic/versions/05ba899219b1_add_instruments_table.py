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

"""Add instruments table

Revision ID: 05ba899219b1
Revises: aed82e046b4f
Create Date: 2016-06-02 00:17:02.405980

"""

# revision identifiers, used by Alembic.
revision = '05ba899219b1'
down_revision = 'aed82e046b4f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'instruments',
        sa.Column('uuid', sa.String(36), primary_key=True),
        sa.Column('_broker_uuid', sa.String(36),
                  sa.ForeignKey('brokers.uuid'),
                  nullable=False,),
        sa.Column('name', sa.String(25), nullable=False, unique=False),
        sa.Column('ticker_symbol', sa.String(10), nullable=False,
                  unique=False, index=True),
        sa.Column('digits', sa.Integer, nullable=False),
        sa.UniqueConstraint('uuid', 'ticker_symbol')
    )


def downgrade():
    op.drop_table('instruments')

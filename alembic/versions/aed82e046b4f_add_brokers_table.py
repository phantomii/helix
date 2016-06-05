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

"""Add brokers table

Revision ID: aed82e046b4f
Revises: 14da048bdb82
Create Date: 2016-06-01 23:51:15.003131

"""

# revision identifiers, used by Alembic.
revision = 'aed82e046b4f'
down_revision = '14da048bdb82'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'brokers',
        sa.Column('uuid', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(72), index=True, nullable=False,
                  unique=True)
    )


def downgrade():
    op.drop_table('brokers')

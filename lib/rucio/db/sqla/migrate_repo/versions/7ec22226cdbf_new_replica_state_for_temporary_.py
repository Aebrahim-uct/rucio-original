# Copyright 2013-2019 CERN for the benefit of the ATLAS collaboration.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors:
# - Martin Barisits <martin.barisits@cern.ch>, 2019
# - Mario Lassnig <mario.lassnig@cern.ch>, 2019
# - Hannes Hansen <hannes.jakob.hansen@cern.ch>, 2019

''' new replica state for temporary unavailable replicas '''

from alembic import context, op
from alembic.op import create_check_constraint, drop_constraint


# Alembic revision identifiers
revision = '7ec22226cdbf'
down_revision = '3345511706b8'

schema = context.get_context().version_table_schema if context.get_context().version_table_schema else ''


def upgrade():
    '''
    Upgrade the database to this revision
    '''

    if context.get_context().dialect.name in ['oracle', 'postgresql', 'mysql']:
        drop_constraint('REPLICAS_STATE_CHK', 'replicas', type_='check')
        create_check_constraint(constraint_name='REPLICAS_STATE_CHK', table_name='replicas',
                                condition="state in ('A', 'U', 'C', 'B', 'D', 'S', 'T')")


def downgrade():
    '''
    Downgrade the database to the previous revision
    '''

    if context.get_context().dialect.name in ['oracle', 'mysql']:
        drop_constraint('REPLICAS_STATE_CHK', 'replicas', type_='check')
        create_check_constraint(constraint_name='REPLICAS_STATE_CHK', table_name='replicas',
                                condition="state in ('A', 'U', 'C', 'B', 'D', 'S')")

    elif context.get_context().dialect.name == 'postgresql':
        op.execute('ALTER TABLE ' + schema + 'replicas DROP CONSTRAINT IF EXISTS "REPLICAS_STATE_CHK", ALTER COLUMN state TYPE CHAR')  # pylint: disable=no-member
        create_check_constraint(constraint_name='REPLICAS_STATE_CHK', table_name='replicas',
                                condition="state in ('A', 'U', 'C', 'B', 'D', 'S')")

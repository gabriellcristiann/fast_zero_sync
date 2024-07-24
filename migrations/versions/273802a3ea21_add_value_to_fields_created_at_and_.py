"""Add value to fields created_at and update_at

Revision ID: 273802a3ea21
Revises: 39579ede3400
Create Date: 2024-07-23 22:16:17.960565

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy.sql.expression import func
from typing import Union, Sequence


# revision identifiers, used by Alembic.
revision: str = '273802a3ea21'
down_revision: Union[str, None] = '39579ede3400'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    todos = table('todos',
                  column('id', sa.Integer),
                  column('created_at', sa.DateTime),
                  column('updated_at', sa.DateTime))

    # Atualizar os valores das colunas com a data e hora atuais
    op.execute(todos.update().values({
        'created_at': func.now(),
        'updated_at': func.now()
    }))

    # Alterar as colunas para serem NOT NULL
    op.alter_column('todos', 'created_at', nullable=False)
    op.alter_column('todos', 'updated_at', nullable=False)


def downgrade():
    # Permitir que as colunas sejam nulas antes de apagar os valores
    op.alter_column('todos', 'created_at', nullable=True)
    op.alter_column('todos', 'updated_at', nullable=True)

    todos = table('todos',
                  column('id', sa.Integer),
                  column('created_at', sa.DateTime),
                  column('updated_at', sa.DateTime))

    # Apagar os valores das colunas
    op.execute(todos.update().values({
        'created_at': None,
        'updated_at': None
    }))
    # ### end Alembic commands ###

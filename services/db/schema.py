from enum import Enum, unique

from sqlalchemy import (
    Table, Column,
    Integer, String, Enum as pgEnum,
    ForeignKeyConstraint, MetaData
)


convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)


@unique
class GlobalRoleEnum(Enum):
    owner = 'owner'
    employee = 'employee'


@unique
class ProjectRoleEnum(Enum):
    admin = 'admin',
    manager = 'manager'


company_table = Table(
    'company', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False)
)

user_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('role', pgEnum(GlobalRoleEnum, name='global_role_enum')),
    Column('company_id', Integer, nullable=False),

    ForeignKeyConstraint(('company_id',), ('company.id',))
)

project_table = Table(
    'project', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(30), nullable=False),
    Column('company_id', Integer, nullable=False),

    ForeignKeyConstraint(('company_id',), ('company.id',))
)

membership_table = Table(
    'membership', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, nullable=False),
    Column('project_id', Integer, nullable=False),
    Column('role', pgEnum(ProjectRoleEnum, name='project_role_enum')),

    ForeignKeyConstraint(('user_id',), ('users.id',)),
    ForeignKeyConstraint(('project_id',), ('project.id',))
)

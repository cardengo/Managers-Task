from random import randint

from tests.utils import exec_query


# --- GENERATE COMPANIES --- #

def generate_companies(nbr=20):
    query = """
        INSERT INTO company(name)
        VALUES('{}')
    """

    queries = []
    for i in range(1, nbr + 1):
        queries.append(
            query.format('company_' + str(i))
        )
    return queries


# --- GENERATE USERS --- #

def generate_users(nbr=20, owner_nbr=2):
    query = """
        INSERT INTO users(name, role, company_id)
        VALUES('{}', '{}', '{}')
    """

    roles = ['employee'] * (nbr - owner_nbr)
    for _ in range(owner_nbr):
        roles.insert(randint(0, nbr), 'owner')

    queries = []
    for i in range(1, nbr + 1):
        queries.append(
            query.format(
                'user_' + str(i),
                roles[i - 1],
                int(randint(1, nbr))
            )
        )
    return queries


# --- GENETATE PROJECTS --- #

def generate_projects(nbr=20):
    query = """
        INSERT INTO project(name, company_id)
        VALUES('{}', '{}')
    """

    queries = []
    for i in range(1, nbr + 1):
        queries.append(
            query.format(
                'project_' + str(i),
                int(randint(1, nbr))
            )
        )
    return queries


# --- GENERATE MEMBERSHIP (dependent data) --- #

SELECT_ALL = """
    SELECT * FROM {}
"""


async def generate_membership():
    admin_nbr = 3

    users_data = await exec_query(SELECT_ALL.format('users'))
    projs_data = await exec_query(SELECT_ALL.format('project'))

    users_ids = [dat['id'] for dat in users_data]
    projs_ids = [dat['id'] for dat in projs_data]

    roles = ['manager'] * (len(users_ids) - admin_nbr)
    for _ in range(admin_nbr):
        roles.insert(randint(0, len(users_ids)), 'admin')

    query = """
        INSERT INTO
        membership(user_id, project_id, role)
        VALUES({}, {}, '{}')
    """

    queries = []
    for _ in range(len(users_ids)):
        queries.append(
            query.format(
                users_ids[randint(0, len(users_ids) - 1)],
                projs_ids[randint(0, len(projs_ids) - 1)],
                roles[randint(0, len(roles) - 1)]
            )
        )
    return queries

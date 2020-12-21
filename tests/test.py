import asyncio

from tests.generate import (
    generate_companies,
    generate_projects,
    generate_users,

    generate_membership
)
from tests.utils import (
    create_postgres,
    drop_postgres,
    exec_query
)


async def exec_queries(queries):
    for query in queries:
        await exec_query(query)


async def create_db_data():
    queries = []

    # GENERATE QUERIES
    queries.append(generate_companies())
    queries.append(generate_users())
    queries.append(generate_projects())

    exec_queries(queries)

    queries = []

    # GENERATE DEPENDENT DATA
    queries.append(await generate_membership())
    exec_queries(queries)


# PASS TESTS
async def test():
    create_postgres()

    # apply_migrations()
    await create_db_data()
    # await pass_test()

    drop_postgres()


asyncio.get_event_loop().run_until_complete(test())

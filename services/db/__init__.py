import pathlib

import asyncpg
# import yaml


DSN = "{RDBMS}://{user}@{host}/{database}"

BASE_DIR = pathlib.Path(__name__).parent.parent
config_path = BASE_DIR / '..' / 'config' / 'db_config.yaml'


def get_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


async def exec_fetch(pool, query):
    res = None
    try:
        async with pool.acquire() as conn:
            res = await conn.fetch(query)
    except Exception as e:
        print('db_api-Exception: ', e)
    return res


async def get_pool():
    # SETUP REQUESTS POOL

    # config = get_config(config_path)
    config = {'postgres': {
          'RDBMS': 'postgresql',
          'database': 'manager_task_db',
          'user': 'nikita',
          'password': '',
          'host': 'localhost',
          'port': ''}
    }

    pool = await asyncpg.create_pool(DSN.format(**config['postgres']))
    return pool

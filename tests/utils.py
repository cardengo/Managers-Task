import asyncpg
import pathlib

from sqlalchemy_utils import create_database, drop_database
import yaml


test_DSN = "{RDBMS}://{user}@{host}/{database}"

BASE_DIR = pathlib.Path(__name__).parent.parent
config_path = BASE_DIR / 'config' / 'test_db_config.yaml'


def get_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


def create_postgres():
    config = get_config(config_path)
    create_database(test_DSN.format(**config['postgres']))


def drop_postgres():
    config = get_config(config_path)
    drop_database(test_DSN.format(**config['postgres']))


async def create_pool():
    config = get_config(config_path)
    pool = await asyncpg.create_pool(test_DSN.format(**config['postgres']))
    return pool


async def exec_query(query):
    pool = await create_pool()

    res = None
    async with pool.acquire() as conn:
        res = await conn.fetch(query)
    await pool.close()
    return res

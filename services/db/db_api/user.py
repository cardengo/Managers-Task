from db import exec_fetch


class User():

    def __init__(self, user_id: int, pool):
        self.pool = pool

        self.user_id = user_id

    def _get_format_lst(self, lst: list) -> str:
        """
        Prepare `list' type data for SQL query.
        """
        formatted_lst = ''
        for data in lst:
            formatted_lst += """{}, """.format(data)
        return formatted_lst[:-2]

    async def _exec_query(self, query) -> list:
        return await exec_fetch(self.pool, query)

    async def get_user_data(self) -> list:
        query = """
            SELECT * FROM users
            WHERE id = '{}'
        """.format(self.user_id)

        return await self._exec_query(query)

    async def get_user_memberships(self) -> list:
        query = """
            SELECT user_id, project_id, role
            FROM membership
            WHERE user_id = '{}'
        """.format(self.user_id)

        return await self._exec_query(query)

    async def get_companies_info(self) -> list:
        """
            Return companies where user works or owns.
        """
        query = """
            SELECT c.id, c.name
            FROM users u
            JOIN company c
            ON u.company_id = c.id
            WHERE u.id = '{}'
        """.format(self.user_id)

        return await self._exec_query(query)

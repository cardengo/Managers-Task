from db import exec_fetch


async def get_instance(user_id: int, pool):
    """
        Get appropriate class instance by global role:
        - owner
        - employee
    """
    instances = {
        'owner': Owner,
        'employee': Employee
    }
    user = User(user_id, pool)
    data = await user.get_user_data()

    return instances.get(str(data[0]['role']))(user_id, pool)


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


class Owner(User):

    async def get_managers(self) -> list:
        companies_info = await self.get_companies_info()
        companies_id = [int(dat['id']) for dat in companies_info]

        formatted_lst = self._get_format_lst(companies_id)

        query = """
            SELECT id, name
            FROM users
            WHERE company_id
            IN ({})
            AND NOT id = '{}'
        """.format(formatted_lst, self.user_id)

        return await self._exec_query(query)


class Employee(User):

    async def get_managers(self) -> list:

        user_memberships = await self.get_user_memberships()
        role = user_memberships[0]['role']

        query = """"""

        if role == 'admin':
            projects_data = await self.get_user_memberships()
            projects_id = [dat['project_id'] for dat in projects_data]

            formatted_lst = self._get_format_lst(projects_id)

            query = """
                SELECT u.id, u.name
                FROM users u
                JOIN membership m
                ON u.id = m.user_id
                WHERE m.project_id IN ({})
                AND m.role = 'manager'
            """.format(formatted_lst)

        if role == 'manager':
            user_data = await self.get_user_data()
            data = {}
            data['id'], data['name'] = user_data[0]['id'], user_data[0]['name']
            return list(user_data)

        return await self._exec_query(query)

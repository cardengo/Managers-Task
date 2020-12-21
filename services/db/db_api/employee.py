from db.db_api.user import User


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

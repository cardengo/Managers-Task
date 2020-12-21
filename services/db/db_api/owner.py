from db.db_api.user import User


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

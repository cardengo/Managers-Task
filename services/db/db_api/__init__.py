from db.db_api.user import User
from db.db_api.owner import Owner
from db.db_api.employee import Employee


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

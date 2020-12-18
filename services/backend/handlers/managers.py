from fastapi import APIRouter, Depends, HTTPException

from backend.models import UserAuthModel
from backend.settings import get_current_username
from db import get_pool
from db.db_api import get_instance


managers_route = APIRouter()


@managers_route.get('/managers')
async def get_managers(
    user_data: UserAuthModel,
    user_id: sorted = Depends(get_current_username)
):
    pool = await get_pool()
    user = await get_instance(int(user_id), pool)
    managers = await user.get_managers()
    pool.close()

    if managers is None:
        raise HTTPException(status_code=500)
    return {'managers': managers}

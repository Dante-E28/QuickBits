from typing import Annotated
from fastapi import APIRouter, Depends

from src.service import UsersService
from src.unitofwork import IUnitOfWork, UnitOfWork
from src.schema import UsersSchema, UsersSchemaAdd


router = APIRouter()
UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


@router.post('', response_model=UsersSchema)
async def create_user(uow: UOWDep, user: UsersSchemaAdd):
    return await UsersService.add_user(uow, user)

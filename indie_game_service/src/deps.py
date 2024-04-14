from typing import Annotated

from fastapi import Depends

from src.unitofwork import IUnitOfWork, UnitOfWork


UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]

from functools import partial
from typing import Callable

from src.repositories.unitofwork import UnitOfWork
from src.users.router import get_me, get_user

uow = UnitOfWork()

functions: dict[str, Callable] = {
    'get_user': partial(get_user, uow=uow),
    'get_me': get_me
}

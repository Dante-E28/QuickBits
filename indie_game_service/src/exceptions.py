from fastapi import HTTPException, status


class EntityNotFoundError(HTTPException):
    def __init__(self, entity_type: str, entity_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{entity_type} id: {entity_id} not found'
        )

class EntityAlreadyExistsError(HTTPException):
    def __init__(self, entity_type: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'{entity_type} already exists'
        )

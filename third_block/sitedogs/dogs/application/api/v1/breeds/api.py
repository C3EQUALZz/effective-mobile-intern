import logging
from uuid import UUID

import anydi
from core.exceptions.base import ApplicationException
from django.http import HttpRequest
from ninja import (
    Query,
    Router,
)
from ninja.errors import HttpError

from dogs.application.api.v1.breeds.schemas import (
    CreateBreedSchemaRequest,
    CreateBreedSchemaResponse,
    GetAllBreedsSchemaResponse,
    GetBreedByOidSchemaResponse,
    UpdateBreedSchemaRequest,
    UpdateBreedSchemaResponse,
)
from dogs.infrastructure.adapters.dto.breeds import BreedWithCountOfDogs
from dogs.logic.commands.breeds import (
    CreateBreedCommand,
    DeleteBreedCommand,
    GetAllBreedsWithCountOfDogsForEachBreedCommand,
    GetBreedByOid,
    UpdateBreedCommand,
)
from dogs.logic.use_cases.breeds import (
    CreateBreedUseCase,
    DeleteBreedUseCase,
    GetAllBreedsWithCountOfDogsForEachBreedUseCase,
    GetBreedByOidUseCase,
    UpdateBreedUseCase,
)

router = Router(tags=["breeds"])
logger = logging.getLogger(__name__)


@router.get("/", summary="get all breeds with count of dogs for each breed", response=list[GetAllBreedsSchemaResponse])
def get_all_breeds(
    request: HttpRequest,
    page_number: int = Query(default=1, required=False, ge=1),
    page_size: int = Query(default=10, required=False, ge=1),
    use_case: GetAllBreedsWithCountOfDogsForEachBreedUseCase = anydi.auto,
):
    """
    Handler for getting all breeds with count of dogs for each breed

    Args:
        request (HttpRequest): HTTP request (needs for Django Ninja)
        page_number (int): Page number for pagination
        page_size (int): Page size for pagination
        use_case: Case that will perform operations
    Returns:
        list with all breeds with count of dogs for each breed
    """
    try:
        command: GetAllBreedsWithCountOfDogsForEachBreedCommand = GetAllBreedsWithCountOfDogsForEachBreedCommand(
            page_number, page_size
        )

        result: list[BreedWithCountOfDogs] = use_case.execute(command=command)
        return [GetAllBreedsSchemaResponse.from_entity(x) for x in result]

    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.post("/", summary="Create a new breed", response=CreateBreedSchemaResponse)
def create_breed(
    request: HttpRequest,
    scheme: CreateBreedSchemaRequest,
    use_case: CreateBreedUseCase = anydi.auto,
):
    """
    Handler for creating a new breed.

    Args:
        request (HttpRequest): HTTP request (needs for Django Ninja).
        scheme (CreateBreedSchemaRequest): scheme that we need for creating new breed.
        use_case (CreateBreedUseCase): use case for creating new breed.

    Returns:
        A new breed which consists oid, name, size, friendliness, train_ability, shedding_amount, exercise_needs
    """
    try:
        return CreateBreedSchemaResponse.from_entity(use_case.execute(CreateBreedCommand(**scheme.model_dump())))
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.get("/{breed_id}", summary="Get a specific breed by his oid", response=GetBreedByOidSchemaResponse)
def get_breed(
    request: HttpRequest,
    breed_id: UUID,
    use_case: GetBreedByOidUseCase = anydi.auto,
):
    """
    Handler for getting a specific breed by his oid.

    Args:
        request (HttpRequest): HTTP request (needs for Django Ninja).
        breed_id (UUID): id of breed
        use_case: UseCase that will perform operations

    Returns:
        A existing breed if oid actual.

    Raises:
        BreedDoesNotExistException if breed with breed_oid does not exist.
    """
    try:
        return GetBreedByOidSchemaResponse.from_entity(use_case.execute(GetBreedByOid(str(breed_id))))
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.put("/{breed_id}", summary="Update a specific breed by his oid", response=UpdateBreedSchemaResponse)
def update_breed(
    request: HttpRequest,
    scheme: UpdateBreedSchemaRequest,
    use_case: UpdateBreedUseCase = anydi.auto,
):
    """
    Handler for updating a specific breed by his oid.

    Args:
        request (HttpRequest): HTTP request (needs for Django Ninja).
        scheme (UpdateBreedSchemaRequest): Scheme that we need for updating new breed. Check attrs in it.
        use_case: UseCase that will perform operations

    Returns:
        Breed that was updated in other case raises BreedDoesNotExistException.

    Raises:
        BreedDoesNotExistException if breed with breed_oid does not exist.
    """
    try:
        return UpdateBreedSchemaResponse.from_entity(use_case.execute(UpdateBreedCommand(**scheme.model_dump())))
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.delete("/{breed_id}", summary="Delete a specific breed by his oid", response=None)
def delete_breed(
    request: HttpRequest,
    breed_id: UUID,
    use_case: DeleteBreedUseCase = anydi.auto,
):
    """
    Handler for deleting a specific breed by his oid.

    Args:
        request (HttpRequest): HTTP request (needs for Django Ninja).
        breed_id (UUID): id of breed
        use_case: UseCase that will perform operations

    Returns:
        None if it was deleted.
    """
    try:
        return use_case.execute(DeleteBreedCommand(str(breed_id)))
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)

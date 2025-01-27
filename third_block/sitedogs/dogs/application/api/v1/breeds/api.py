import logging

from django.http import HttpRequest

import anydi
from dogs.application.api.v1.breeds.schemas import (
    CreateBreedSchemaRequest,
    CreateBreedSchemaResponse,
    GetAllBreedsSchemaResponse,
    GetBreedByOidSchemaResponse,
    UpdateBreedSchemaRequest,
    UpdateBreedSchemaResponse,
)
from dogs.exceptions.base import ApplicationException
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
from ninja import (
    Query,
    Router,
)
from ninja.errors import HttpError


router = Router(tags=['breeds'])
logger = logging.getLogger(__name__)


@router.get(
    '/',
    summary="get all breeds with count of dogs for each breed",
    response=list[GetAllBreedsSchemaResponse]
)
def get_all_breeds(
        request: HttpRequest,  # noqa
        page_number: int = Query(default=1, required=False, ge=1),
        page_size: int = Query(default=10, required=False, ge=1),
        use_case: GetAllBreedsWithCountOfDogsForEachBreedUseCase = anydi.auto
):
    try:
        command: GetAllBreedsWithCountOfDogsForEachBreedCommand = GetAllBreedsWithCountOfDogsForEachBreedCommand(
            page_number,
            page_size
        )

        result: list[BreedWithCountOfDogs] = use_case.execute(command=command)
        return [GetAllBreedsSchemaResponse.from_entity(x) for x in result]

    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.post(
    "/",
    summary="Create a new breed",
    response=CreateBreedSchemaResponse
)
def create_breed(
        request: HttpRequest,  # noqa
        scheme: CreateBreedSchemaRequest,
        use_case: CreateBreedUseCase = anydi.auto
):
    try:
        return CreateBreedSchemaResponse.from_entity(use_case.execute(CreateBreedCommand(**scheme.model_dump())))
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.get(
    '/{breed_id}',
    summary="Get a specific breed by his oid",
    response=GetBreedByOidSchemaResponse
)
def get_breed(
        request: HttpRequest, # noqa
        breed_id: str,
        use_case: GetBreedByOidUseCase = anydi.auto
):
    try:
        return GetBreedByOidSchemaResponse.from_entity(use_case.execute(GetBreedByOid(breed_id)))
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.put(
    '/{breed_id}',
    summary="Update a specific breed by his oid",
    response=UpdateBreedSchemaResponse
)
def update_breed(
        request: HttpRequest, # noqa
        scheme: UpdateBreedSchemaRequest,
        use_case: UpdateBreedUseCase = anydi.auto
):
    try:
        return UpdateBreedSchemaResponse.from_entity(use_case.execute(UpdateBreedCommand(**scheme.model_dump())))
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.delete(
    '/{breed_id}',
    summary="Delete a specific breed by his oid",
    response=None
)
def delete_breed(
        request: HttpRequest,  # noqa
        breed_id: str,
        use_case: DeleteBreedUseCase = anydi.auto
):
    try:
        return use_case.execute(DeleteBreedCommand(breed_id))
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)

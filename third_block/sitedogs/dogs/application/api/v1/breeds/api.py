import logging

import anydi
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from dogs.application.api.v1.breeds.schemas import CreateBreedSchemaRequest, UpdateBreedSchemaRequest, \
    CreateBreedSchemaResponse
from dogs.exceptions.base import ApplicationException
from dogs.logic.commands.breeds import CreateBreedCommand, DeleteBreedCommand, \
    GetAllBreedsWithCountOfDogsForEachBreedCommand, GetBreedByOid, UpdateBreedCommand
from dogs.logic.use_cases.breeds import CreateBreedUseCase, DeleteBreedUseCase, \
    GetAllBreedsWithCountOfDogsForEachBreedUseCase, GetBreedByOidUseCase, UpdateBreedUseCase

router = Router(tags=['breeds'])
logger = logging.getLogger(__name__)


@router.get('/')
def get_all_breeds(
        request: HttpRequest,  # noqa
        page_number: int = 0,
        page_size: int = 10,
        use_case: GetAllBreedsWithCountOfDogsForEachBreedUseCase = anydi.auto
):
    try:
        return use_case.execute(GetAllBreedsWithCountOfDogsForEachBreedCommand(page_number, page_size))
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
)
def get_breed(
        request: HttpRequest, # noqa
        breed_id: str,
        use_case: GetBreedByOidUseCase = anydi.auto
):
    try:
        return use_case.execute(GetBreedByOid(breed_id))
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.put(
    '/{breed_id}',
    summary="Update a specific breed by his oid",
)
def update_breed(
        request: HttpRequest, # noqa
        scheme: UpdateBreedSchemaRequest,
        use_case: UpdateBreedUseCase = anydi.auto
):
    try:
        return use_case.execute(UpdateBreedCommand(**scheme.model_dump()))
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.delete('/{breed_id}')
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

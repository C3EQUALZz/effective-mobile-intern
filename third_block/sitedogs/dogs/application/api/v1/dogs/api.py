import logging

import anydi
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from dogs.application.api.v1.dogs.schemas import CreateDogSchemaRequest, CreateDogSchemaResponse
from dogs.exceptions.base import ApplicationException
from dogs.logic.commands.dogs import CreateDogCommand
from dogs.logic.use_cases.dogs import CreateDogUseCase, GetDogByOidWithNumberOfSameBreedUseCase, \
    GetAllDogsWithAverageAgeForEachBreedUseCase, DeleteDogUseCase

router = Router(tags=['dogs'])
logger = logging.getLogger(__name__)


@router.get(
    '/',
    summary="Gets all dogs with average age for each breed"
)
def get_all_dogs(
        request: HttpRequest,  # noqa
        page_number: int = 0,
        page_size: int = 10,
        use_case: GetAllDogsWithAverageAgeForEachBreedUseCase = anydi.auto
):
    try:
        return use_case.execute(page_number, page_size)
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.post(
    '/',
    summary="Handler for creating a dog",
    response=CreateDogSchemaResponse,
)
def create_dog(
        request: HttpRequest,  # noqa
        scheme: CreateDogSchemaRequest,
        use_case: CreateDogUseCase = anydi.auto
):
    try:
        return use_case.execute(CreateDogCommand(**scheme.model_dump()))
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.get('/{dog_id}')
def get_dog_by_id(
        request: HttpRequest,  # noqa
        dog_id: str,
        use_case: GetDogByOidWithNumberOfSameBreedUseCase = anydi.auto
):
    try:
        return use_case.execute(dog_id)
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.put('/{dog_id}')
def update_dog(
        request: HttpRequest,  # noqa
        dog_id: int
):
    ...


@router.delete(
    '/{dog_id}',
    summary="Handler for deleting a dog",
    response=None,
)
def delete_dog(
        request: HttpRequest,  # noqa
        dog_id: str,
        use_case: DeleteDogUseCase = anydi.auto
):
    return use_case.execute(dog_id)

import logging

from django.http import HttpRequest

import anydi
from dogs.application.api.v1.dogs.schemas import (
    CreateDogSchemaRequest,
    CreateDogSchemaResponse,
    GetAllDogsWithAverageAgeForEachBreedSchemeResponse,
    GetDogByOidSchemaResponse,
    UpdateDogSchemaRequest,
    UpdateDogSchemaResponse,
)
from dogs.exceptions.base import ApplicationException
from dogs.infrastructure.adapters.dto.dogs import DogsWithAverageAgeForEachBreed
from dogs.logic.commands.dogs import (
    CreateDogCommand,
    DeleteDogCommand,
    UpdateDogCommand,
)
from dogs.logic.use_cases.dogs import (
    CreateDogUseCase,
    DeleteDogUseCase,
    GetAllDogsWithAverageAgeForEachBreedUseCase,
    GetDogByOidWithNumberOfSameBreedUseCase,
    UpdateDogUseCase,
)
from ninja import (
    Query,
    Router,
)
from ninja.errors import HttpError


router = Router(tags=["dogs"])
logger = logging.getLogger(__name__)


@router.get(
    "/",
    summary="Handler for get all dogs with average age for each breed",
    response=list[GetAllDogsWithAverageAgeForEachBreedSchemeResponse],
)
def get_all_dogs(
    request: HttpRequest,  # noqa
    page_number: int = Query(default=1, required=False, ge=1),
    page_size: int = Query(default=1, required=False, ge=1),
    use_case: GetAllDogsWithAverageAgeForEachBreedUseCase = anydi.auto,
):
    try:
        result: list[DogsWithAverageAgeForEachBreed] = use_case.execute(page_number, page_size)
        return [GetAllDogsWithAverageAgeForEachBreedSchemeResponse.from_entity(x) for x in result]
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.post(
    "/",
    summary="Handler for creating a dog",
    response=CreateDogSchemaResponse,
)
def create_dog(
    request: HttpRequest,  # noqa
    scheme: CreateDogSchemaRequest,
    use_case: CreateDogUseCase = anydi.auto,
):
    try:
        return CreateDogSchemaResponse.from_entity(use_case.execute(CreateDogCommand(**scheme.model_dump())))
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.get("/{dog_id}", summary="Handler for gets a dog by id", response=GetDogByOidSchemaResponse)
def get_dog_by_id(
    request: HttpRequest,  # noqa
    dog_id: str,
    use_case: GetDogByOidWithNumberOfSameBreedUseCase = anydi.auto,
):
    try:
        return GetDogByOidSchemaResponse.from_entity(use_case.execute(dog_id))
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.put("/{dog_id}", summary="Handler for updating a dog by id", response=UpdateDogSchemaResponse)
def update_dog(
    request: HttpRequest,  # noqa
    scheme: UpdateDogSchemaRequest,
    use_case: UpdateDogUseCase = anydi.auto,
):
    try:
        command: UpdateDogCommand = UpdateDogCommand(**scheme.model_dump())
        return UpdateDogSchemaResponse.from_entity(use_case.execute(command))
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)


@router.delete(
    "/{dog_id}",
    summary="Handler for deleting a dog",
    response=None,
)
def delete_dog(
    request: HttpRequest,  # noqa
    dog_id: str,
    use_case: DeleteDogUseCase = anydi.auto,
):
    try:
        return use_case.execute(DeleteDogCommand(dog_id))
    except ApplicationException as e:
        logger.error(e)
        raise HttpError(e.status, e.message)

from django.http import HttpRequest
from ninja import Router

router = Router(tags=['dogs'])


@router.get('/')
def get_all_dogs(
        request: HttpRequest,
):
    ...


@router.post('/')
def create_dog(request: HttpRequest):
    ...


@router.get('/{dog_id}')
def get_dog_by_id(request: HttpRequest, dog_id: int):
    ...


@router.put('/{dog_id}')
def update_dog(request: HttpRequest, dog_id: int):
    ...


@router.delete('/{dog_id}')
def delete_dog(request: HttpRequest, dog_id: int):
    ...

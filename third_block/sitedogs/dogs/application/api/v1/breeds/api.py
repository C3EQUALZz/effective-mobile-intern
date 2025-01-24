from django.http import HttpRequest
from ninja import Router

router = Router(tags=['breeds'])


@router.get('/')
def get_all_breeds(request: HttpRequest):
    ...


@router.post("/")
def create_breed(request: HttpRequest):
    ...


@router.get('/{breed_id}')
def get_breed(request: HttpRequest, breed_id: int):
    ...


@router.put('/{breed_id}')
def update_breed(request: HttpRequest, breed_id: int):
    ...


@router.delete('/{breed_id}')
def delete_breed(request: HttpRequest, breed_id: int):
    ...

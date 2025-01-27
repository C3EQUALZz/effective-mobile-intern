from dogs.application.api.v1.breeds.api import router as breeds_router
from dogs.application.api.v1.dogs.api import router as dogs_router
from ninja import NinjaAPI


api = NinjaAPI(
    title="API for Dogs",
    version="1.0.0",
    description="This API is for 3rd block of internship",
)

api.add_router(prefix="/dogs/", router=dogs_router)
api.add_router(prefix="/breeds/", router=breeds_router)

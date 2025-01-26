from django.contrib import admin

from dogs.infrastructure.adapters.django_orm.orm import Dog, Breed

# Register your models here.
admin.site.register(Dog)
admin.site.register(Breed)

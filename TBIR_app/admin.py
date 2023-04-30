from django.contrib import admin
from TBIR_app.models import Photo

# Register your models here.


@admin.register(Photo)
class PHotoAdmin(admin.ModelAdmin):
    pass

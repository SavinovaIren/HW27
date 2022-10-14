from django.contrib import admin

from ads.models import *

# Register your models here.
admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(User)

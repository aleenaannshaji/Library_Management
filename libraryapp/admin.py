from django.contrib import admin
from django.urls import path, include
from .models import Studentreg, Staffreg, Program, Department, Designation, Book


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('libraryapp.urls')),
]


admin.site.register(Studentreg)
admin.site.register(Staffreg)
admin.site.register(Program)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Book)
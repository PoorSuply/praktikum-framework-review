from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models.teachers import Teachers
from .models.students import Students
from .models.users import Users

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('nip', 'name', 'email', 'phone_number')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        user, created = Users.objects.get_or_create(username=obj.nip, defaults={
        'password': make_password('default_password'),
        'role': Users.TEACHER })
        if not created:
            user.role = Users.TEACHER
            user.save()

admin.site.register(Teachers, TeacherAdmin)
admin.site.register(Students)
admin.site.register(Users)
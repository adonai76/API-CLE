from django.contrib import admin
from .models import Career, StudentProfile, TeacherProfile, Coordinator  

# Register your models here.
admin.site.site_header = "Administración del Sistema CLE"

admin.site.register(Career)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)


@admin.register(Coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name")
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=True).exclude(is_superuser=True)

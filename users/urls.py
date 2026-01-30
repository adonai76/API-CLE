from django.urls import path, include
from .views import StudentRegisterView, TeacherRegisterView, CareerViewSet, CoordinatorRegisterView  
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'careers', CareerViewSet, basename='career')

urlpatterns = [
    # Ruta para alumnos: /api/users/register/student/
    path("register/student/", StudentRegisterView.as_view(), name="student-register"),
    # Ruta para docentes: /api/users/register/teacher/
    path("register/teacher/", TeacherRegisterView.as_view(), name="teacher-register"),
    # Ruta para coordinadores: /api/users/register/coordinator/
    path("register/coordinator/", CoordinatorRegisterView.as_view(), name="coordinator-register"),
    # Ruta para carreras: /api/users/careers/
    path("", include(router.urls)),
    
]

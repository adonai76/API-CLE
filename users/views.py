from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth.models import User
from .models import Career
from .serializers import (
    StudentRegisterSerializer, 
    TeacherRegisterSerializer,
    CareerSerializer,
    CoordinatorRegisterSerializer
)

# 1. VISTAS DE REGISTRO 

class StudentRegisterView(generics.CreateAPIView):
    """
    Endpoint público para registrar nuevos alumnos.
    """
    queryset = User.objects.all() # DRF necesita saber en qué base de datos buscar, aunque sea creación
    permission_classes = [AllowAny] # Configuración de permisos: acceso público
    serializer_class = StudentRegisterSerializer

class TeacherRegisterView(generics.CreateAPIView):
    """
    Endpoint público para registrar nuevos docentes.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny] # Acceso público
    serializer_class = TeacherRegisterSerializer

class CareerViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para Carreras.
    Solo el Staff (Coordinadores) debería poder crear/borrar aquí.
    """
    queryset = Career.objects.all()
    serializer_class = CareerSerializer
    permission_classes = [IsAdminUser] 

class CoordinatorRegisterView(generics.CreateAPIView):
    """
    Vista exclusiva para administradores.
    Permite crear nuevos usuarios con rol de Staff (Coordinadores).
    """
    serializer_class = CoordinatorRegisterSerializer
    permission_classes = [IsAdminUser] # Solo admins pueden entrar aquí
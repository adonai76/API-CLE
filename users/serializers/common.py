from rest_framework import serializers
from django.contrib.auth.models import User, Group


# SERIALIZER BASE & UTILIDADES
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer anidado para validar datos de usuario.
    """

    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }


class BaseRegistrationSerializer(serializers.ModelSerializer):
    """
    Clase Abstracta (Mixin) que contiene la lógica común para crear usuarios.
    No se usa directamente, sino que los demás heredan de ella.
    """

    def create_user_with_group(self, user_data, group_name, is_staff=False):
        """
        Método auxiliar para:
        1. Encriptar contraseña.
        2. Crear usuario.
        3. Asignar estatus de staff.
        4. Asignar grupo.
        """
        password = user_data.pop("password")
        user = User(**user_data)
        user.set_password(password)
        user.is_staff = is_staff
        user.save()

        # Asignación automática de Grupo
        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        return user

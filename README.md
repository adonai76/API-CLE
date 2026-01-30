# API – Sistema de Gestión CLE (ITL)

Este repositorio contiene el **Backend y la lógica de servidor** del sistema administrativo de la **Coordinación de Lenguas Extranjeras (CLE)** del Instituto Tecnológico de León.

La API está diseñada bajo una arquitectura **cliente–servidor**, exponiendo endpoints REST seguros para ser consumidos por aplicaciones web o móviles.

---

## Función del Repositorio

Proveer endpoints que permitan a las aplicaciones cliente:

* Gestionar usuarios (alumnos, docentes y coordinadores).
* Registrar y administrar perfiles académicos.
* Subir y validar evidencias y documentación de docentes o alumnos.
* Administrar grupos, horarios y procesos académicos.
* Procesar captura y consulta de calificaciones.

---

## Stack Tecnológico

| Componente           | Tecnología                  |
| -------------------- | --------------------------- |
| Lenguaje             | Python 3.x                  |
| Framework            | Django 5.x                  |
| API Toolkit          | Django REST Framework (DRF) |
| Autenticación        | JWT (JSON Web Tokens)       |
| Base de Datos (Dev)  | SQLite                      |
| Base de Datos (Prod) | PostgreSQL                  |
| Gestión de Paquetes  | pip + requirements.txt      |

---

## Estructura General del Proyecto

```text
cle_project/
├── manage.py
├── requirements.txt
├── README.md
├── config/                  # Configuración principal del proyecto
├── apps/
│   ├── users/               # Usuarios, perfiles y autenticación
│   ├── academics/           # Grupos, materias, inscripciones
│   ├── payments/            # Pagos
│   └── grades/              # Calificaciones
└── media/                   # Archivos subidos (evidencias)
```

**Nota:** La estructura puede crecer conforme se agreguen nuevos módulos.

---

## Configuración del Entorno (Desarrollo)

Sigue estos pasos para levantar el proyecto en tu máquina local.

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-organizacion/api-cle.git
cd api-cle
```

---

### 2. Crear y activar entorno virtual

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido (no subir al repositorio):

```env
DEBUG=True
SECRET_KEY=tu_clave_secreta_segura
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

### 5. Migraciones y Superusuario

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

El servidor estará disponible en:

```
http://127.0.0.1:8000/
```

---

## Documentación de la API

Una vez corriendo el servidor, puedes acceder a la documentación interactiva:

* **Swagger UI:** [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
* **ReDoc:** [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)

---

## Contribución

1. Hacer un fork del repositorio.
2. Crear una rama para tu feature:

   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Hacer commit de tus cambios:

   ```bash
   git commit -m "Agrega nueva funcionalidad"
   ```
4. Hacer push a la rama:

   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. Abrir un Pull Request.

---

## Autoría

Desarrollado por el equipo del Instituto Tecnológico de León (ITL) – 2026.

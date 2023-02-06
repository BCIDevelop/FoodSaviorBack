# Boilerplate Flask

---

## Modulos

1. Usuarios
2. Roles
3. Autenticación

## Modelos

```sql
-- Usuarios
- id
- name
- last_name
- username
- password
- email
- rol_id
- status

-- Roles
- id
- name
- status
```

## Caracteristicas

1. Login
   - [x] Creación de token (JWT - JSONWEBTOKEN | access_token, refresh_token).
   - [x] Validación de contraseñas encriptadas (bcrypt).
2. Registro
   - [x] Encriptación de contraseñas (bcrypt).
3. Recuperar contraseña
   - [x] Generar una contraseña nueva.
   - [x] Enviar un correo con un template, mencionando la contraseña generada.
4. CRUD para cada Modelo
   - [x] Listado con paginación (Obtener los datos relacionados).
   - [x] Obtener registro por id (Obtener los datos relacionados).
   - [x] Creación de registro.
   - [x] Actualización de registro.
   - [x] Eliminar registro (SOFTDELETE).
5. Decoradores
   - [x] Proteger rutas con autenticación.
   - [x] Proteger rutas por rol.
6. Documentación y Validaciones
   - [x] Swagger
   - [x] Schemas
7. Despliegue
   - [Render](https://render.com/)

## Recursos

### Contenido de archivo .env

```py
FLASK_APP='main.py'
FLASK_DEBUG=True
FLASK_RUN_HOST=127.0.0.1
FLASK_RUN_PORT=5000
ENVIRONMENT='development'

DATABASE_URL='postgresql://postgres:mysql@localhost:5432/flask_boilerplate'

JWT_SECRET='tecsup'

MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=''
MAIL_PASSWORD=''
```

### Documentación

- SQLAlchemy
  - [Metodos usados para el modelo](https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.all)
  - [Tipo de datos](https://docs.sqlalchemy.org/en/14/core/types.html)
  - [Nuevos metodos para el modelo](https://github.com/absent1706/sqlalchemy-mixins/blob/master/README.md)
- FlaskRestX
  - [Tipo de datos](https://flask-restx.readthedocs.io/en/latest/_modules/flask_restx/fields.html)
  - [Response](https://flask-restx.readthedocs.io/en/latest/marshalling.html)
  - [Request Parsing](https://flask-restx.readthedocs.io/en/latest/parsing.html)
  - [Swagger](https://flask-restx.readthedocs.io/en/latest/swagger.html)
- FlaskJWTExtended
  - [BlackList](https://flask-jwt-extended.readthedocs.io/en/stable/blocklist_and_token_revoking/)
  - [Proteccion de rutas](https://flask-jwt-extended.readthedocs.io/en/stable/optional_endpoints/)

### Conexión URI a PGSQL

```py
postgresql://usuario:password@ip_servidor:puerto/nombre_bd
```

### Migraciones

- Iniciar las migraciones (Ejecuta una sola vez)

```sh
flask db init
```

- Crear una migración (Cuando se crea un modelo nuevo o se modifica uno anterior)

```sh
flask db migrate -m "Comentario"
```

- Subir los cambios a nuestra BD

```sh
flask db upgrade
```

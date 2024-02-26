
# Portal de Autoatención



## Despliegue

Para comenzar a ejecutar el proyecto, seguir los siguientes pasos:

- Instalar los paquetes de python requeridos para el proyecto (de preferencia en un entorno virtual).
```bash
  pip install -r requirements.txt
```

- Inicializar el contenedor de docker con la base de datos de postgresql.

```bash
  docker-compose up
```

- Realizar las migraciones de las bases de datos de proyectos compartidos.

```bash
  py manage.py makemigrations clientManager
  py manage.py makemigrations loginApp
  py manage.py makemigrations solicitudesManager

```

- Con la base de datos en pie, migrar los modelos

```bash
  py manage.py migrate_schemas --shared
  py manage.py migrate_schemas

```
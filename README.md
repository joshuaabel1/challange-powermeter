# Challange-powermeter

## Solution to Powermeter challenge:


### Para correr el proyecto, sigue los siguientes pasos:


1) Primero creamos el entorno

```
python -m venv env-powermeter
env-powermeter\Scripts\activate
```
Instalamos las dependencias

En la raiz del proyecto.

PASO 1: 
Abrir una terminal en la carpeta del proyecto

```
docker compose up -d
```

Paso 2:
Obtener el ContainerId del service "web"

```
docker ps
```

insertar captura de pantalla para mostrar cual es el ID a copiar

ingresar al service "web" y ejecutar el comando reemplazando <WebContainerId> por el CONTAINER_ID copiado en el paso anterior

```
docker exec -it <WebContainerId> bash
```

recolectar migraciones

```
python3 manage.py makekigrations
```

ejecutar migraciones

```
python3 manage.py migrate
```

correr los test

``` 
python3 manage.py test meters
```

### Endpoints

Crear un nuevo medidor:

Para crear un nuevo medidor, hacer una petición HTTP POST a la url /meter/ con un JSON válido en el cuerpo de la petición.

Ejemplo:

```
POST /meter/
Content-Type: application/json

{
    "name": "Medidor A"
}
```

Crear una nueva medición:

Para crear una nueva medición, hacer una petición HTTP POST a la url /measurement/ con un JSON válido en el cuerpo de la petición.

Ejemplo:

```
POST /measurement/
Content-Type: application/json

{
    "meter": 1,
    "consumption": 10.5
}
```

Obtener medición máxima:

Para obtener la medición máxima de un medidor específico, hacer una petición HTTP GET a la url `/measurement/[id_del_medidor]/max/.

Ejemplo:

```
GET /measurement/12/max/
Content-Type: application/json

{
    "meter": 12,
    "reading_datetime": "2023-01-12T00:11:36.872197Z",
    "consumption": 3.6
}
```
Obtener medición mínima:

Para obtener la medición mínima de un medidor específico, hacer una petición HTTP GET a la url /measurement/[id_del_medidor]/min/, donde [id_del_medidor] es el id del medidor para el cual se desea obtener la medición mínima.

Ejemplo:

```
GET /measurement/12/min/
Content-Type: application/json
{
    "meter": 12,
    "reading_datetime": "2023-01-11T23:53:58.003909Z",
    "consumption": 1.4
}
```

Obtener consumo total:

Para obtener el consumo total de un medidor específico, hacer una petición HTTP GET a la url /meters/[id_del_medidor]/total_consumption/, donde [id_del_medidor] es el id.

Ejemplo:

```
GET /meters/12/total_consumption/
Content-Type: application/json

{
    "sum_of_consumption": 5.0
}
```
Obtener consumo promedio:

Para obtener el consumo promedio de un medidor específico, enviar una petición GET a la url "/measurement/[id_del_medidor]/average_consumption/", reemplazando [id_del_medidor] con el id del medidor deseado. La respuesta incluirá el consumo promedio en el formato "avg_of_consumption": [valor].

Ejemplo:

```
GET /measurement/12/average_consumption/
Content-Type: application/json

{
    "avg_of_consumption": 2.5
}
```

### Defensa del modelo de estructura:

La estructura elegida es la básica de Django, con un archivo de test que sirve como guía para la creación de los endpoints. En caso de requerir más aplicaciones se podría crear una carpeta adicional (apps) para alojar estas y dividir el archivo settings para adaptarlo a las diferentes instancias del proyecto. Esto permite una fácil escalabilidad y organización del proyecto en caso de necesitar agregar más funcionalidades en el futuro.

```
powermeter/
    manage.py
    myproject/
        __init__.py
        urls.py
        asgi.py
        wsgi.py
        settings/
            __init__.py
            base.py
            local.py
            prod.py
    apps/
        __init__.py
        meters/
            __init__.py
            admin.py
            models.py
            serializer.py
            tests.py
            views.py
        auth/
            __init__.py
            admin.py
            models.py
            serializer.py
            tests.py
            views.py
    media/
    static/
```
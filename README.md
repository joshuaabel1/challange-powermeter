# Challange-powermeter

## Solution to Powermeter challenge:


### Para correr el proyecto, sigue los siguientes pasos:


1) Primero creamos el entorno

```
python -m venv env-powermeter
env-powermeter\Scripts\activate
```
2) Instalamos las dependencias
```
pip install -r requirements.txt
```
3) Creamos las tablas en la base de datos
```
python manage.py makemigrations
python manage.py migrate
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

Para obtener la medición máxima de un medidor específico, hacer una petición HTTP GET a la url `/measurement/[id_del_medidor]/.

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

Tests :

``` 
python manage.py test meters
```

Iniciar contenedor:

En la raiz del proyecto.

``` 
docker compose up
``` 

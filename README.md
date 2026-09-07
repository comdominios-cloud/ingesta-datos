# ingesta-datos

Tres contenedores Python que hacen **pull del 100% de los registros** de las
bases de los microservicios y los suben como **CSV/JSON a un bucket S3**.

> CS2032 Cloud Computing - UTEC | Proyecto: Sistema de Administracion de Condominios

## Responsable

[@carloscondor1610](https://github.com/carloscondor1610) — Data Science. Ver [INTEGRANTE.md](INTEGRANTE.md).

Integrante a cargo de **data science**, junto con
[`ms-analitico`](../ms-analitico), que consulta con Athena lo que aqui se sube.

## Dominio

Alimenta el data lake del proyecto. Cada carpeta es un contenedor independiente
con su propio Dockerfile:

| Contenedor | Origen | Motor | Datos | Formato en S3 |
|------------|--------|-------|-------|---------------|
| `ingesta01` | ms-residentes | **PostgreSQL** 5432 | edificios, unidades, residentes, usuarios | CSV |
| `ingesta02` | ms-pagos | **MySQL** 3306 | cuotas, pagos | CSV |
| `ingesta03` | ms-incidencias | MongoDB 27017 | incidencias, reservas | JSON |

```
VM de base de datos          VM de ingesta
  PostgreSQL :5432  ──────>  ingesta01 ─┐
  MySQL      :3306  ──────>  ingesta02 ─┼──> s3://BUCKET/raw/<contenedor>/
  MongoDB    :27017 ──────>  ingesta03 ─┘              │
                                                       ▼
                                        Glue crawler ──> Athena ──> ms-analitico :9005
```

`ingesta03` es el que alimenta la prediccion de **que area comun sera la mas
visitada el proximo mes**, porque las reservas viven en MongoDB.

## Stack

| Elemento | Tecnologia |
|----------|------------|
| Lenguaje | Python 3.12 |
| SDK AWS | boto3 |
| Drivers | psycopg / pymysql / pymongo |
| Orquestacion | Docker Compose (3 servicios) |

## Puertos

Ninguno: son **jobs batch**, no exponen HTTP. Corren, suben a S3 y terminan.
Los puertos del proyecto (para referencia): ms-residentes 9001, ms-pagos 9002,
ms-incidencias 9003, ms-ficha-residente 9004, ms-analitico 9005,
web-condominio 5173 (dev). Las bases que lee esta ingesta: PostgreSQL 5432,
MySQL 3306, MongoDB 27017.

## Variables de entorno

Copiar [.env.example](.env.example) a `.env` y completar. Un solo `.env` en la raiz
alimenta a los 3 contenedores. **Nunca** commitear `.env` ni credenciales.

| Variable | Descripcion |
|----------|-------------|
| `AWS_REGION` | Region de AWS |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` / `AWS_SESSION_TOKEN` | Credenciales (usar IAM Role en EC2) |
| `S3_BUCKET` | Bucket destino |
| `S3_PREFIX` | Prefijo dentro del bucket (`raw/`) |
| `POSTGRES_HOST` / `POSTGRES_PORT` / `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` | Conexion de ingesta01 (IP privada de la VM de base de datos) |
| `MYSQL_HOST` / `MYSQL_PORT` / `MYSQL_DATABASE` / `MYSQL_USER` / `MYSQL_PASSWORD` | Conexion de ingesta02 |
| `MONGO_URI` / `MONGO_DB` | Conexion de ingesta03 |

## Como levantar con Docker

Para el avance del 50% alcanza con **uno solo**, el de PostgreSQL:

```bash
cp .env.example .env
docker compose up --build ingesta01
```

Los tres a la vez:

```bash
cp .env.example .env      # completar credenciales
docker compose up --build
```

O sin compose:

```bash
docker build -t ingesta01 ./ingesta01
docker run --rm --env-file .env ingesta01
```

Las imagenes se publican en **Docker Hub** para que la VM de ingesta haga `pull`
en vez de construir:

```bash
docker build -t <usuario>/ingesta01:0.1.0 ./ingesta01
docker push <usuario>/ingesta01:0.1.0
```

## Estructura

```
docker-compose.yml    # levanta los 3 contenedores
.env.example          # variables compartidas
ingesta01/            # PostgreSQL -> CSV -> S3
├── Dockerfile
├── requirements.txt
└── ingesta.py        # placeholder
ingesta02/            # MySQL -> CSV -> S3       (misma estructura)
ingesta03/            # MongoDB -> JSON -> S3     (misma estructura)
```

## Estado

Andamiaje inicial. Los tres `ingesta.py` son placeholders sin logica de
extraccion ni subida a S3.

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
| `ingesta01` | ms-residentes | MySQL | edificios, unidades, residentes | CSV |
| `ingesta02` | ms-pagos | PostgreSQL | cuotas, pagos | CSV |
| `ingesta03` | ms-incidencias | MongoDB | incidencias, reservas | JSON |

```
MySQL ──> ingesta01 ─┐
PostgreSQL ──> ingesta02 ─┼──> s3://BUCKET/raw/ ──> Glue crawler ──> Athena ──> ms-analitico
MongoDB ──> ingesta03 ─┘
```

## Stack

| Elemento | Tecnologia |
|----------|------------|
| Lenguaje | Python 3.12 |
| SDK AWS | boto3 |
| Drivers | pymysql / psycopg2 / pymongo |
| Orquestacion | Docker Compose (3 servicios) |

## Puertos

Ninguno: son **jobs batch**, no exponen HTTP. Corren, suben a S3 y terminan.
Los puertos del proyecto (para referencia): ms-residentes 8001, ms-pagos 8002,
ms-incidencias 8003, ms-ficha-residente 8004, ms-analitico 8005,
web-condominio 5173 (dev).

## Variables de entorno

Copiar [.env.example](.env.example) a `.env` y completar. Un solo `.env` en la raiz
alimenta a los 3 contenedores. **Nunca** commitear `.env` ni credenciales.

| Variable | Descripcion |
|----------|-------------|
| `AWS_REGION` | Region de AWS |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` / `AWS_SESSION_TOKEN` | Credenciales (usar IAM Role en EC2) |
| `S3_BUCKET` | Bucket destino |
| `S3_PREFIX` | Prefijo dentro del bucket (`raw/`) |
| `MYSQL_HOST` / `MYSQL_PORT` / `MYSQL_DATABASE` / `MYSQL_USER` / `MYSQL_PASSWORD` | Conexion de ingesta01 |
| `POSTGRES_HOST` / `POSTGRES_PORT` / `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` | Conexion de ingesta02 |
| `MONGO_URI` / `MONGO_DB` | Conexion de ingesta03 |

## Como levantar con Docker

Los tres a la vez:

```bash
cp .env.example .env      # completar credenciales
docker compose up --build
```

Uno solo:

```bash
docker compose up --build ingesta01
```

O sin compose:

```bash
docker build -t ingesta01 ./ingesta01
docker run --rm --env-file .env ingesta01
```

## Estructura

```
docker-compose.yml    # levanta los 3 contenedores
.env.example          # variables compartidas
ingesta01/            # MySQL -> CSV -> S3
├── Dockerfile
├── requirements.txt
└── ingesta.py        # placeholder
ingesta02/            # PostgreSQL -> CSV -> S3  (misma estructura)
ingesta03/            # MongoDB -> JSON -> S3    (misma estructura)
```

## Estado

Andamiaje inicial. Los tres `ingesta.py` son placeholders sin logica de
extraccion ni subida a S3.

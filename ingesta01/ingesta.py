"""ingesta01 | ms-residentes (PostgreSQL) -> S3.

PLACEHOLDER. Debe extraer el 100% de los registros de edificios, unidades, residentes y usuarios
y subirlos al bucket S3 en formato CSV.

Uso previsto:
    python ingesta.py
"""


def main() -> None:
    # TODO: 1. Leer configuracion (conexion y S3) desde variables de entorno.
    # TODO: 2. Conectar a PostgreSQL (VM de base de datos, puerto 5432).
    # TODO: 3. Extraer el 100% de los registros de edificios, unidades, residentes y usuarios (paginado por lotes).
    # TODO: 4. Escribir el resultado en CSV.
    # TODO: 5. Subir a s3://$S3_BUCKET/$S3_PREFIX<tabla>/ con boto3.
    raise NotImplementedError("Pendiente de implementar en la fase de ingesta.")


if __name__ == "__main__":
    main()

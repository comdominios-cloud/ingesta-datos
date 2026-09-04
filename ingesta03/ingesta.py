"""ingesta03 | ms-incidencias (MongoDB) -> S3.

PLACEHOLDER. Debe extraer el 100% de los registros de incidencias y reservas
y subirlos al bucket S3 en formato JSON.

Uso previsto:
    python ingesta.py
"""


def main() -> None:
    # TODO: 1. Leer configuracion (conexion y S3) desde variables de entorno.
    # TODO: 2. Conectar a MongoDB.
    # TODO: 3. Extraer el 100% de los registros de incidencias y reservas (paginado por lotes).
    # TODO: 4. Escribir el resultado en JSON.
    # TODO: 5. Subir a s3://$S3_BUCKET/$S3_PREFIX<tabla>/ con boto3.
    raise NotImplementedError("Pendiente de implementar en la fase de ingesta.")


if __name__ == "__main__":
    main()

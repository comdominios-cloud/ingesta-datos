import csv
import os
from pathlib import Path
from tempfile import TemporaryDirectory

import boto3
import psycopg
from psycopg import sql
from dotenv import load_dotenv


# La tabla `usuarios` ya NO vive en condominio_residentes: se movio a la base
# condominio_usuarios cuando usuarios paso a ser su propio microservicio.
# Se puede sobreescribir con la variable INGESTA_TABLAS (separadas por coma).
TABLAS_POR_DEFECTO = ("edificios", "unidades", "residentes")
TAMANO_LOTE = 1000


def tablas_a_exportar():
    configuradas = os.getenv("INGESTA_TABLAS", "").strip()

    if configuradas:
        return tuple(t.strip() for t in configuradas.split(",") if t.strip())

    return TABLAS_POR_DEFECTO


def variable(nombre):
    valor = os.getenv(nombre)
    if not valor:
        raise ValueError(f"Falta configurar {nombre}")
    return valor


def exportar_tabla(conn, tabla, carpeta):
    # Obtener las columnas, excluyendo el hash de contraseña.
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = %s
              AND column_name <> 'password_hash'
            ORDER BY ordinal_position
            """,
            (tabla,),
        )
        columnas = [fila[0] for fila in cur.fetchall()]

    if not columnas:
        # No cortamos la ingesta por una tabla que no existe: se avisa y se
        # sigue con el resto. Cortar aqui significaria no subir NADA a S3,
        # porque la subida ocurre recien despues de extraer todo.
        print(f"Aviso: la tabla {tabla} no existe en esta base, se omite", flush=True)
        return None, 0

    consulta = sql.SQL("SELECT {} FROM {} ORDER BY {}").format(
        sql.SQL(", ").join(sql.Identifier(c) for c in columnas),
        sql.Identifier("public", tabla),
        sql.Identifier("id"),
    )

    ruta = carpeta / f"{tabla}.csv"
    total = 0

    # Cursor del servidor para leer por lotes.
    with conn.cursor(name=f"exportar_{tabla}") as cur:
        cur.execute(consulta)

        with ruta.open("w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(columnas)

            while True:
                filas = cur.fetchmany(TAMANO_LOTE)
                if not filas:
                    break

                escritor.writerows(filas)
                total += len(filas)

    print(f"Extraído: {tabla} | {total} registros", flush=True)
    return ruta, total


def main():
    load_dotenv()

    bucket = variable("S3_BUCKET")
    prefijo = variable("S3_PREFIX").strip("/")
    s3 = boto3.client("s3", region_name=variable("AWS_REGION"))

    with TemporaryDirectory() as temporal:
        carpeta = Path(temporal)
        archivos = []

        with psycopg.connect(
            host=variable("POSTGRES_HOST"),
            port=variable("POSTGRES_PORT"),
            dbname=variable("POSTGRES_DB"),
            user=variable("POSTGRES_USER"),
            password=variable("POSTGRES_PASSWORD"),
            connect_timeout=10,
        ) as conn:
            # Todas las tablas se leen desde una misma instantánea.
            conn.execute(
                "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY"
            )

            for tabla in tablas_a_exportar():
                ruta, total = exportar_tabla(conn, tabla, carpeta)

                if ruta is not None:
                    archivos.append((tabla, ruta, total))

        if not archivos:
            raise RuntimeError(
                "No se exporto ninguna tabla: revisar INGESTA_TABLAS y la base configurada"
            )

        # Subir únicamente después de completar la extracción.
        for tabla, ruta, total in archivos:
            clave = f"{prefijo}/{tabla}/{tabla}.csv"
            s3.upload_file(
                str(ruta),
                bucket,
                clave,
                ExtraArgs={"ContentType": "text/csv; charset=utf-8"},
            )
            print(
                f"Subido: s3://{bucket}/{clave} | {total} registros",
                flush=True,
            )

    print(
        f"Ingesta completada: {len(archivos)} tablas exportadas y subidas.",
        flush=True,
    )


if __name__ == "__main__":
    main()

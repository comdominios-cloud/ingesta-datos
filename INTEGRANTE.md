# Integrante responsable

| | |
|---|---|
| **Repositorio** | `ingesta-datos` |
| **Integrante** | [@carloscondor1610](https://github.com/carloscondor1610) |
| **Rol** | Data Science |
| **Puerto** | ninguno (jobs batch) |

## Alcance

`ingesta-datos`: los 3 contenedores Python que vuelcan las bases a S3. Va junto con [ms-analitico](https://github.com/comdominios-cloud/ms-analitico), que consulta lo que aqui se sube.

> ### Prioridad del avance del 50%
>
> El ACL pidio, en este orden:
>
> 1. Crear la **VM EC2 de ingesta** con Ubuntu 22.04
> 2. Crear el **bucket S3**
> 3. Que alguien levante la **base PostgreSQL** (es @Osomar1705)
> 4. Vincular esa base con la VM de ingesta
> 5. Que la ingesta suba el archivo al bucket
>
> **Un solo contenedor** por ahora: `ingesta01`, el de PostgreSQL. Los otros dos
> y todo lo de Glue/Athena van despues.

## Avance del 50% — entrega del 6 al 12 de septiembre

- [listo ] **VM EC2 de ingesta** con Ubuntu 22.04 y Docker
- [] **Bucket S3** creado, con una carpeta por contenedor
- [ ] Security Group de la VM: salida a 5432 hacia la VM de base de datos, salida 443 hacia S3
- [ ] `ingesta01` conectado al **PostgreSQL de @Osomar1705**
- [ ] Extraccion de los registros y generacion del **CSV/JSON**
- [ ] Archivo subido a su carpeta del bucket
- [ ] **Evidencia**: captura de los datos almacenados en S3
- [ ] Imagen en **Docker Hub**

### Despues del avance

- [ ] `ingesta02` (MySQL) e `ingesta03` (MongoDB)
- [ ] Pull del **100%** de los registros, no una muestra

---

## Como trabajamos

Cada repositorio pertenece a un integrante y se desarrolla de forma
**independiente**: las APIs con base de datos no se llaman entre si. La unica
integracion entre microservicios vive en `ms-ficha-residente`, y la del lado del
usuario en `web-condominio`.

Los cambios a este repositorio los define su responsable. Si otro integrante
necesita algo de esta API, se pide via issue en vez de tocar el codigo.

## Equipo

| Repositorio | Integrante | Rol | Puerto |
|---|---|---|---|
| [ms-residentes](https://github.com/comdominios-cloud/ms-residentes) | @Osomar1705 | API con BD - Python / PostgreSQL | 9001 |
| [ms-pagos](https://github.com/comdominios-cloud/ms-pagos) | @sebastianperez72 | API con BD - Java / MySQL | 9002 |
| [ms-incidencias](https://github.com/comdominios-cloud/ms-incidencias) | @fabianbot1331 | API con BD - lenguaje por definir / MongoDB | 9003 |
| [ms-ficha-residente](https://github.com/comdominios-cloud/ms-ficha-residente) | @Brisseth-raton | Backend / Infraestructura | 9004 |
| [web-condominio](https://github.com/comdominios-cloud/web-condominio) | @alxgr-08 | Frontend / Amplify | 5173 (dev) |
| [ms-analitico](https://github.com/comdominios-cloud/ms-analitico) | @carloscondor1610 | Data Science | 9005 |
| [ingesta-datos](https://github.com/comdominios-cloud/ingesta-datos) | @carloscondor1610 | Data Science | — |

> CS2032 Cloud Computing - UTEC | Sistema de Administracion de Condominios

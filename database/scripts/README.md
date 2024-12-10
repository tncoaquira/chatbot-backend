# Instalación de la Base de Datos

## Para entornos de `producción`

Las instrucciones y comandos utilizados para crear desde cero la Base de Datos del proyecto se encuentra en el archivo [dbcreate.sql](./dbcreate.sql).

## Para entornos de `desarrollo` (con docker)

La creacion del contenedor y inicializacion de postgres se encuentra en [docker-compose.yml](../../docker-compose.yml)
```bash
# Crea una instancia de postgres
docker compose up -d
```
Donde: `pg16` es el nombre del contenedor.

## Para entornos de `desarrollo` (Con postgres nativo)

Se requiere tener instalado postgres a nivel del sistema operativo con la siguiente configuración:

```bash
# Archivo /etc/postgresql/16/main/pg_hba.conf
local   all     postgres                    md5
```

Ahora si, procedemos a crear la base de datos

```bash
psql -U postgres -f dbcreate.sql
```


--CREATE DATABASE chatbot_db
--CREATE DATABASE record_manager_db


DO $$
BEGIN
    -- crear la base    
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'chatbot_db') THEN
        CREATE DATABASE chatbot_db ENCODING 'UTF8';
    END IF;
    -- configuramos la zona horaria (solo es necesario si utilizamos docker)
    ALTER ROLE postgres SET TIMEZONE TO 'America/La_Paz';

    -- creamos los esquemas correspondientes
    CREATE SCHEMA IF NOT EXISTS conocimiento;
    CREATE SCHEMA IF NOT EXISTS autentificacion;
    
END $$


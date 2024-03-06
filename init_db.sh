# init db
sudo -u huan1531 psql -d postgres <<PGSCRIPT
DROP DATABASE IF EXISTS baran_sparcle;
CREATE DATABASE baran_sparcle;
DROP USER IF EXISTS baranuser;
CREATE USER baranuser;
ALTER USER baranuser WITH PASSWORD 'baranpass';
GRANT ALL PRIVILEGES ON DATABASE baran_sparcle TO baranuser ;
\c baran_sparcle
GRANT ALL ON SCHEMA public TO baranuser;
CREATE EXTENSION postgis;
PGSCRIPT

echo "DB baran_sparcle created/reset."
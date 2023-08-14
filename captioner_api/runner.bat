@echo off

REM DATABASE
set DB_NAME=zoiadb
set DB_USER=postgres
set DB_PASSWORD=pass

REM SECURITY
set SECRET_KEY=7b32ce61ba1791759c068c4705fa6fe010e906f672524d0e83b6162cb284f36d
set DECODE_ALGORITHM=HS256


REM DOCKER COMMAND
docker run -d --name zoia ^
  -e POSTGRES_USER=%DB_USER% ^
  -e POSTGRES_PASSWORD=%DB_PASSWORD% ^
  -e POSTGRES_DB=%DB_NAME% ^
  -p 5432:5432 postgres

echo Environment configured, running project.

REM RUN PROJECT
set RESTART_DATABASE=False
python app.py
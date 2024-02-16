:: DATABASE
set DB_NAME=zoiadb
set DB_USER=postgres
set DB_PASSWORD=pass
set DB_URI=sqlite:///zoia.sqlite

:: SECURITY
set SECRET_KEY=7b32ce61ba1791759c068c4705fa6fe010e906f672524d0e83b6162cb284f36d
set DEFAULT_ACCESS_TOKEN=9c0503cad7176e02bac7d2b411c592db
set DECODE_ALGORITHM=HS256

echo Environment configured, running project.

:: RUN PROJECT
set RESTART_DATABASE=False
set FLASK_APP=app

flask run --debug
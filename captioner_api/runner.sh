# DATABASE
export DB_NAME="zoiadb"
export DB_USER="postgres"
export DB_PASSWORD="pass"
export DB_URI="sqlite:///zoia.sqlite"

# SECURITY
export SECRET_KEY="7b32ce61ba1791759c068c4705fa6fe010e906f672524d0e83b6162cb284f36d"
export DEFAULT_ACCESS_TOKEN="9c0503cad7176e02bac7d2b411c592db"
export DECODE_ALGORITHM="HS256"

echo "Environment configured, running project."

# RUN PROJECT
export RESTART_DATABASE="False"
export FLASK_APP="app"

flask run --debug
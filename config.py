from os import environ

db_host = environ.get('DB_HOST', default='')
db_name = environ.get('DB_NAME', default='dashboard')
db_pass = environ.get('DB_PASS', default='')
db_port = environ.get('DB_PORT', default='5432')
db_user = environ.get('DB_USER', default='dashboard')

SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

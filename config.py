conn_string = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'.format(
user = 'postgres', 
password = 'l,kmazsx1',
host = 'localhost',
port = '5432',
dbname = 'first_database')

DEBUG = True
SQLALCHEMY_DATABASE_URI = conn_string
SECRET_KEY = 'GF9zHFS-cSXQyxN31zCmjg'
SQLALCHEMY_TRACK_MODIFICATIONS =  False # silence the deprecation warning
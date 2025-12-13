from os import getenv
from dotenv import load_dotenv
import psycopg2 as pg

load_dotenv()

db_user = getenv('USER_NAME')
user_password = getenv('USER_PASSWORD')
db_host = getenv('DB_HOST')
db_port = getenv('DB_PORT')
db_name = getenv('DB_DJANGO')



conn = pg.connect(
    user = db_user,
    password = user_password,
    host = db_host,   
    port =  db_port,
    dbname = db_name
 
)


cur = conn.cursor()
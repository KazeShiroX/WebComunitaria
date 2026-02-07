import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('DB_HOST', 'localhost')
user = os.getenv('DB_USER', 'root')
password = os.getenv('DB_PASSWORD', '')
port = int(os.getenv('DB_PORT', 3306))
dbname = os.getenv('DB_NAME', 'comunidad_bd')

print(f"Testing connection to {host} as {user}...")

try:
    # Connect without DB name first to check auth
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port
    )
    print("Connection successful!")
    
    with connection.cursor() as cursor:
        print(f"Creating database {dbname} if not exists...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbname} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    
    connection.commit()
    connection.close()
    print("Database preparation complete.")
except Exception as e:
    print(f"Error: {e}")

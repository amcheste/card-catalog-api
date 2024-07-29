import os


DB_HOST = os.getenv('DB_HOST', default='127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', default=5432))
DB_NAME = os.getenv('DB_NAME', default='card-catalog')
DB_USER = os.getenv('DB_USER', default='card-catalog')
DB_PASSWORD = os.getenv('DB_PASSWORD', default='password')
